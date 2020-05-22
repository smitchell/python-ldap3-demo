#!/usr/bin/env python3
import logging

from confuse import Configuration
from typing import Any
from flask import Response
from ldap3 import Connection, ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES, DEREF_NEVER, DEREF_SEARCH, DEREF_BASE, \
    DEREF_ALWAYS, BASE, LEVEL, SUBTREE, MODIFY_ADD, MODIFY_DELETE, MODIFY_REPLACE, MODIFY_INCREMENT
from ldap3.core.exceptions import LDAPInvalidDnError
from ldap3.utils.conv import escape_filter_chars
from ldap3_demo.controllers.connection_manager import ConnectionManager
from ldap3_demo.dtos.add_entry_request import AddEntryRequest
from ldap3_demo.dtos.modify_entry_request import ModifyEntryRequest
from ldap3_demo.dtos.search import Search

dereference_aliases_types = dict(
    DEREF_NEVER=DEREF_NEVER,
    DEREF_SEARCH=DEREF_SEARCH,
    DEREF_BASE=DEREF_BASE,
    DEREF_ALWAYS=DEREF_ALWAYS
)

operation_types = dict(
    MODIFY_ADD=MODIFY_ADD,
    MODIFY_DELETE=MODIFY_DELETE,
    MODIFY_REPLACE=MODIFY_REPLACE,
    MODIFY_INCREMENT=MODIFY_INCREMENT
)

search_scope_types = dict(BASE=BASE, LEVEL=LEVEL, SUBTREE=SUBTREE)


class LdapController:

    def __init__(self):
        config = Configuration('ldap3_demo', __name__)
        self.connection_manager = ConnectionManager(config.get(dict))

    # This method adds a new entry to LDAP. The dn must be unique and must match the dn
    # attribute in the AddEntryRequest.
    def add(self, server_name: str, add_entry_request: AddEntryRequest):
        connection: Connection = self.connection_manager.get_connection(server_name, None)
        connection.bind()

        if add_entry_request.controls is None:
            if add_entry_request.attributes is not None:
                connection.add(add_entry_request.dn, add_entry_request.object_class,
                               LdapController.scrub_dict(add_entry_request.attributes, True),
                               add_entry_request.controls)
            else:
                connection.add(add_entry_request.dn, add_entry_request.object_class, None, add_entry_request.controls)
        elif add_entry_request.attributes is not None:
            connection.add(add_entry_request.dn, add_entry_request.object_class,
                           LdapController.scrub_dict(add_entry_request.attributes, True))
        else:
            connection.add(add_entry_request.dn, add_entry_request.object_class)

        result_description = connection.result["description"]
        if result_description == 'entryAlreadyExists':
            msg = f'{add_entry_request.dn} {result_description}: {connection.last_error}'
            logging.error(msg)
            return Response(
                msg,
                status=400,
            )

        if result_description != 'success':
            msg = f'An error occurred: {result_description}: {connection.last_error}'
            logging.error(msg)
            return Response(
                msg,
                status=500,
            )

        return True

    # This method modifies an existing entry ing LDAP. The dn must match an existing entity.
    def modify(self, server_name: str, modify_entry_request: ModifyEntryRequest) -> bool:
        connection: Connection = self.connection_manager.get_connection(server_name, None)
        connection.bind()
        changes = modify_entry_request.changes
        for attribute_key in changes:
            attribute = changes[attribute_key]
            temp_dict = {}
            result = []
            for operation in attribute:
                for operation_key in operation.keys():
                    new_key = operation_types[operation_key]
                    if new_key in temp_dict:
                        temp_dict[new_key] += operation[operation_key]
                    else:
                        temp_dict[new_key] = operation[operation_key]

            for key in temp_dict.keys():
                result.append(tuple([key] + temp_dict[key]))
            changes[attribute_key] = result

        if modify_entry_request.controls is not None:
            connection.modify(modify_entry_request.dn, changes, modify_entry_request.controls)
        else:
            connection.modify(modify_entry_request.dn, changes)

        result_description = connection.result["description"]
        if result_description != 'success':
            logging.error(f'The modify failed: {result_description}')
            return False

        return True

    def search(self, server_name: str, s: Search) -> list:
        connection: Connection = self.connection_manager.get_connection(server_name, None)
        connection.bind()
        connection.search(search_base=s.search_base,
                          search_filter=s.search_filter,
                          search_scope=search_scope_types[s.search_scope],
                          dereference_aliases=dereference_aliases_types[s.dereference_aliases],
                          attributes=LdapController._convert_attributes_keyword(s.attributes),
                          size_limit=s.size_limit,
                          time_limit=s.time_limit,
                          types_only=s.types_only,
                          get_operational_attributes=s.get_operational_attributes,
                          controls=s.controls,
                          paged_size=s.paged_size,
                          paged_criticality=s.paged_criticality,
                          paged_cookie=s.paged_cookie)
        print(connection)
        if connection.result is None:
            return []
        if 'description' in connection.result:
            description = connection.result['description']
            if description == 'success':
                return self._convert_results(connection.entries)
            elif description == 'noSuchObject':
                return []
        msg = f'Unknown search result: {connection.result}'
        logging.error(msg)
        return [msg]

    def delete(self, server_name: str, dn: Any, controls: Any = None) -> bool:
        connection: Connection = self.connection_manager.get_connection(server_name, None)
        connection.bind()

        try:
            connection.delete(dn, controls=controls)
            return True
        except LDAPInvalidDnError:
            # Ignore error if the dn does not exist.
            logging.warning(f'{dn} could not be found to delete.')
            return True

    @staticmethod
    def _convert_results(entries) -> list:
        results = []
        if entries is not None:
            for entry in entries:
                results.append({'dn': entry.entry_dn, 'attributes': entry.entry_attributes_as_dict})
        return results

    @staticmethod
    def _convert_attributes_keyword(value) -> Any:
        if value == 'ALL_ATTRIBUTES':
            return ALL_ATTRIBUTES
        if value == 'ALL_OPERATION_ATTRIBUTES':
            return ALL_OPERATIONAL_ATTRIBUTES
        return value

    @staticmethod
    def scrub_json(source) -> None:
        if 'controls' in source:
            controls = source['controls']
            if controls is None or controls == 'None' or len(controls) == 0:
                del source['controls']
        if 'attributes' in source:
            attributes = source['attributes']
            if attributes is None or attributes == 'None' or len(attributes) == 0:
                del source['attributes']
            else:
                # The dn of add_entry_request and modify entry request
                # don't pass validation so only process the attributes.
                attributes = source['attributes']
                for key in attributes:
                    attributes[key] = escape_filter_chars(attributes[key])

    @staticmethod
    def scrub_dict(source, remove_empty: bool = False):
        target = {}
        for key in source:
            value = escape_filter_chars(source[key])
            if remove_empty and (value is None or value == 'None' or len(value) == 0):
                continue
            target[key] = value
        return target

