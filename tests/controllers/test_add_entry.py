
from ldap3_demo.schemas.add_entry_request_schema import AddEntryRequestSchema
from ldap3 import Server, Connection, MOCK_SYNC, ALL_ATTRIBUTES, BASE

server = Server('my_fake_server')
schema = AddEntryRequestSchema()


def test_add_with_valid_data():

    connection = Connection(server, user='cn=my_user,ou=test,o=lab', password='my_password', client_strategy=MOCK_SYNC)
    connection.bind()

    dn = 'cn=employees,ou=test,o=lab'
    connection.add(dn, 'organizationalUnit')
    result_description = connection.result["description"]
    assert result_description == 'success', f'Add {dn} failed.{result_description}'
    assert connection.last_error is None, f'An error occurred adding {dn}.{connection.last_error}'
    print(f'Successfully added {dn}')

    dn = 'cn=users,cn=employees,ou=test,o=lab'
    connection.add(dn, 'organizationalUnit')
    assert result_description == 'success', f'Add {dn} failed.{result_description}'
    assert connection.last_error is None, f'An error occurred adding {dn}.{connection.last_error}'
    print(f'Successfully added {dn}')

    dn = 'cn=user0,cn=users,cn=employees,ou=test,o=lab'
    connection.add(dn, 'inetOrgPerson', {'userPassword': 'test0000', 'sn': 'user0_sn'})
    assert result_description == 'success', f'Add {dn} failed.{result_description}'
    assert connection.last_error is None, f'An error occurred adding {dn}.{connection.last_error}'
    print(f'Successfully added {dn}')

    connection.search(search_base=dn,
                               search_filter='(objectClass=inetOrgPerson)',
                               search_scope=BASE,
                               attributes=ALL_ATTRIBUTES)
    assert result_description == 'success', f'Searching for {dn} failed.{result_description}'
    assert connection.last_error is None, f'An error occurred searching for {dn}.{connection.last_error}'
    total_results = len(connection.entries)
    assert total_results == 1, f'Expected 1 search result for {dn} but found {total_results}'

    dn = 'cn=user1,cn=users,cn=employees,ou=test,o=lab'
    print(f'Adding {dn}')
    connection.add(dn, 'inetOrgPerson',
                                           {
                                               'userPassword': 'test0000',
                                               'sn': 'user1_sn'})
    assert result_description == 'success', f'Add {dn} failed.{result_description}'
    assert connection.last_error is None, f'An error occurred adding {dn}.{connection.last_error}'
    print(f'Successfully added {dn}')

    connection.search(search_base=dn,
                               search_filter='(objectClass=inetOrgPerson)', search_scope=BASE,
                               attributes=ALL_ATTRIBUTES)
    assert result_description == 'success', f'Searching for {dn} failed.{result_description}'
    assert connection.last_error is None, f'An error occurred searching for {dn}.{connection.last_error}'
    total_results = len(connection.entries)
    assert total_results == 1, f'Expected 1 search result for {dn} but found {total_results}'

    dn = 'cn=user2,cn=users,cn=employees,ou=test,o=lab'
    connection.add(dn, 'inetOrgPerson',
                                           {
                                               'userPassword': 'test0000',
                                               'sn': 'user2_sn'})
    assert result_description == 'success', f'Add {dn} failed.{result_description}'
    assert connection.last_error is None, f'An error occurred adding {dn}.{connection.last_error}'
    print(f'Successfully added {dn}')

    connection.search(search_base=dn,
                               search_filter='(objectClass=inetOrgPerson)', search_scope=BASE,
                               attributes=ALL_ATTRIBUTES)
    assert result_description == 'success', f'Searching for {dn} failed.{result_description}'
    assert connection.last_error is None, f'An error occurred searching for {dn}.{connection.last_error}'
    total_results = len(connection.entries)
    assert total_results == 1, f'Expected 1 search result for {dn} but found {total_results}'
    person = connection.entries[0]

    # data = {
    #     'basedn': 'ou=test,o=lab',
    #     'dn': 'cn=mwatkins,cn=users,cn=employees,ou=test,o=lab',
    #     # 'object_class': 'top,person,organizationalPerson,inetOrgPerson',
    #     'object_class': 'inetOrgPerson',
    #     'attributes': {
    #         'o': 'lab',
    #         'ou': 'test'
    #     }
    # }
    #
    # controller = LdapController()
    # add_entry_request = schema.load(data)
    # controller.add(connection, add_entry_request)
    # dn = add_entry_request.dn
    # assert result_description == 'success', f'Searching for {dn} failed.{result_description}'
    # assert connection.last_error is None, f'An error occurred searching for {dn}.{connection.last_error}'
    # total_results = len(connection.entries)
    # assert total_results == 1, f'Expected 1 search result for {dn} but found {total_results}'
