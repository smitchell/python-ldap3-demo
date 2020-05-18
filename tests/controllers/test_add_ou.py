#!/usr/bin/env python3
from typing import Union
from ldap3_demo.app import connection_manager
from ldap3_demo.controllers.ldap_controller import LdapController
from ldap3_demo.schemas.add_entry_request_schema import AddEntryRequestSchema
from ldap3_demo.schemas.search_schema import SearchSchema

schema = AddEntryRequestSchema()

def test_add_user_with_controller():

    # Pass the new employees data to the controller
    controller = LdapController()
    add_entry_request = schema.load({
        'dn': 'cn=employees,ou=test,o=lab',
        'object_class': 'organizationalUnit'
    })
    result = controller.add(connection_manager.mocked, add_entry_request)
    assert result, 'There was a problem adding {add_entry_request.dn}'

    dn = add_entry_request.dn
    data = {
        'search_base': dn,
        'search_filter': '(objectClass=organizationalUnit)',
        'search_scope': 'SUBTREE'
    }
    search_schema = SearchSchema()
    results = controller.search(connection_manager.mocked, search_schema.load(data))
    total_results = len(results)
    assert total_results == 1, f'Expected 1 search result for {dn} but found {total_results}'

    add_entry_request = schema.load({
        'dn': 'cn=users,cn=employees,ou=test,o=lab',
        'object_class': 'organizationalUnit'
    })

    result = controller.add(connection_manager.mocked, add_entry_request)
    dn = add_entry_request.dn
    assert result, 'There was a problem adding {dn}'

    data = {
        'search_base': dn,
        'search_filter': '(objectClass=organizationalUnit)',
        'search_scope': 'SUBTREE'
    }
    search_schema = SearchSchema()
    results = controller.search(connection_manager.mocked, search_schema.load(data))
    total_results = len(results)
    assert total_results == 1, f'Expected 1 search result for {dn} but found {total_results}'
