#!/usr/bin/env python3
import logging
from confuse import Configuration
from typing import Any
from typing import List
from typing import Optional
from flask import Response
from ldap3 import Connection
from ldap3.core.exceptions import LDAPInvalidDnError
from ldap3.utils.conv import escape_filter_chars
from ldap3_demo.controllers.connection_manager import ConnectionManager
from ldap3_demo.dtos.add_entry_request import AddEntryRequest
from ldap3_demo.dtos.modify_entry_request import ModifyEntryRequest
from ldap3_demo.dtos.search import Search
from ldap3.abstract.entry import Entry
import json


class LdapController:

    def __init__(self):
        config = Configuration('ldap3_demo', __name__)
        self.connection_manager = ConnectionManager(config['ldap'].get(dict))

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
        print(f'remove_empty -> {remove_empty}')
        for key in source:
            value = escape_filter_chars(source[key])
            if remove_empty and (value is None or value == 'None' or len(value) == 0):
                continue
            target[key] = value
        return target

    # This method adds a new entry to LDAP. The dn must be unique and must match the dn
    # attribute in the AddEntryRequest.
    def add(self, server_name: str, add_entry_request: AddEntryRequest) -> bool:
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
            return Response(
                f'The dn {add_entry_request.dn} already exists: {connection.last_error}',
                status=400,
            )

        if result_description != 'success':
            return Response(
                f'An error occurred: {connection.last_error}',
                status=500,
            )

        return True

    # This method modifies an existing entry ing LDAP. The dn must match an existing entity.
    def modify(self, server_name: str, modify_entry_request: ModifyEntryRequest) -> bool:
        connection: Connection = self.connection_manager.get_connection(server_name, None)
        connection.bind()
        changes = modify_entry_request.changes

        if modify_entry_request.controls is not None:
            connection.modify(modify_entry_request.dn, changes, modify_entry_request.controls)
        else:
            connection.modify(modify_entry_request.dn, changes)

        result_description = connection.result["description"]
        if result_description != 'success':
            return Response(
                f'An error occurred: {connection.last_error}',
                status=500,
            )

        return True

    def search(self, server_name: str, s: Search) -> List[Optional[Any]]:
        connection: Connection = self.connection_manager.get_connection(server_name, None)
        connection.bind()
        connection.search(search_base=s.search_base,
                          search_filter=s.search_filter,
                          search_scope=s.search_scope,
                          dereference_aliases=s.dereference_aliases,
                          attributes=s.attributes,
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
            print('connection result is None')
            return []
        if 'description' in connection.result:
            description = connection.result['description']
            print(f'Description: {description}')
            if description == 'success':
                logging.warning(f'Entries --> {connection.entries}')
                return self._convert_results(connection.entries)
            elif description != 'noSuchObject':
                return Response(f'A search error occurred: {description}', status=500)

        return []

    def delete(self, server_name: str, dn: Any, controls: Any = None) -> bool:
        connection: Connection = self.connection_manager.get_connection(server_name, None)
        connection.bind()
        try:
            connection.delete(dn, controls=controls)
            return True
        except LDAPInvalidDnError:
            # Ignore error if the dn does not exist.
            return True

    @staticmethod
    def _convert_results(entries) -> list:
        results = []
        if entries is not None:
            for entry in entries:
                my_entry = entry.entry_to_json()
                results.append(json.loads(my_entry))
        return results
