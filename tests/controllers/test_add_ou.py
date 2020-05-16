#!/usr/bin/env python3

from ldap3_demo.controllers.ldap_controller import LdapController
from ldap3_demo.schemas.add_entry_request_schema import AddEntryRequestSchema
from ldap3 import Server, Connection, MOCK_SYNC, ALL_ATTRIBUTES, BASE

server = Server('my_fake_server')
schema = AddEntryRequestSchema()


def test_add_user_with_controller():

    connection = Connection(server, user='cn=my_user,ou=test,o=lab', password='my_password', client_strategy=MOCK_SYNC)
    connection.bind()

    # Pass the new employees data to the controller
    controller = LdapController()
    add_entry_request = schema.load({
        'dn': 'cn=employees,ou=test,o=lab',
        'object_class': 'organizationalUnit'
    })
    result = controller.add(connection, add_entry_request)
    assert result, 'There was a problem adding {add_entry_request.dn}'

    dn = add_entry_request.dn
    connection.search(search_base=dn,
                      search_filter='(objectClass=organizationalUnit)',
                      search_scope=BASE,
                      attributes=ALL_ATTRIBUTES)
    result_description = connection.result["description"]
    assert result_description == 'success', f'Searching for {dn} failed. {result_description}'
    assert connection.last_error is None, f'An error occurred searching for {dn}. {connection.last_error}'
    total_results = len(connection.entries)
    assert total_results == 1, f'Expected 1 search result for {dn} but found {total_results}'

    add_entry_request = schema.load({
        'dn': 'cn=users,cn=employees,ou=test,o=lab',
        'object_class': 'organizationalUnit'
    })

    result = controller.add(connection, add_entry_request)
    dn = add_entry_request.dn
    assert result, 'There was a problem adding {dn}'

    connection.search(search_base=dn,
                      search_filter='(objectClass=organizationalUnit)',
                      search_scope=BASE,
                      attributes=ALL_ATTRIBUTES)
    result_description = connection.result["description"]
    assert result_description == 'success', f'Searching for {dn} failed. {result_description}'
    assert connection.last_error is None, f'An error occurred searching for {dn}. {connection.last_error}'
    total_results = len(connection.entries)
    assert total_results == 1, f'Expected 1 search result for {dn} but found {total_results}'