#!/usr/bin/env python3

from typing import Any
from flask import Response
from ldap3 import Connection
from ldap3.core.exceptions import LDAPInvalidDnError
from ldap3.utils.conv import escape_filter_chars
from ldap3_demo.dtos.add_entry_request import AddEntryRequest
from ldap3_demo.dtos.modify_entry_request import ModifyEntryRequest
from ldap3_demo.dtos.search import Search
from ldap3_demo.schemas.add_entry_request_schema import AddEntryRequestSchema
from ldap3_demo.schemas.modify_entry_request_schema import ModifyEntryRequestSchema


class LdapController:

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
    def add(self, connection: Connection, add_entry_request: AddEntryRequest) -> bool:
        schema = AddEntryRequestSchema()

        json = schema.dump(add_entry_request)

        if 'controls' in json:
            if 'attributes' in json and json['attributes'] is not None:
                connection.add(add_entry_request.dn, json['object_class'],
                               LdapController.scrub_dict(json['attributes'], True), json['controls'])
            else:
                connection.add(add_entry_request.dn, json['object_class'], None, json['controls'])
        elif 'attributes' in json and json['attributes'] is not None:
            connection.add(add_entry_request.dn, json['object_class'],
                           LdapController.scrub_dict(json['attributes'], True))
        else:
            connection.add(add_entry_request.dn, json['object_class'])

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
    def modify(self, connection: Connection, modify_entry_request: ModifyEntryRequest) -> bool:
        schema = ModifyEntryRequestSchema()
        changes = modify_entry_request['changes']

        json = schema.dump(modify_entry_request)
        if 'controls' in json:
            connection.modify(modify_entry_request.dn, modify_entry_request['changes'], json['controls'])
        else:
            connection.modify(modify_entry_request.dn, modify_entry_request['changes'])

        result_description = connection.result["description"]
        if result_description != 'success':
            return Response(
                f'An error occurred: {connection.last_error}',
                status=500,
            )

        return True

    def search(self, connection: Connection, s: Search) -> list:
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
        if connection.result["description"] != 'success':
            return Response(
                f'A search error occurred: {connection.last_error}',
                status=500,
            )

        return connection.entries

    def delete(self, connection: Connection, dn: Any, controls: Any = None) -> bool:
        try:
            return connection.delete(dn, controls=controls)
        except LDAPInvalidDnError:
            # Ignore error if the dn does not exist.
            return True
