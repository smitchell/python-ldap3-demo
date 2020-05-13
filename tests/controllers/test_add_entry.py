import sys

from ldap3_demo.controllers.ldap_controller import LdapController
from ldap3_demo.schemas.add_entry_request_schema import AddEntryRequestSchema
from ldap3 import Server, Connection, MOCK_SYNC, ALL_ATTRIBUTES, BASE, SUBTREE
from ldap3.utils.log import set_library_log_detail_level, set_library_log_hide_sensitive_data, OFF, BASIC, NETWORK, \
    EXTENDED, set_library_log_activation_level

import logging

logging.basicConfig(filename='/Users/stevemitchell/Development/python_projects/python-ldap3-demo/ldap.log',
                    level=logging.CRITICAL)

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
root.addHandler(handler)
set_library_log_activation_level(logging.CRITICAL)

set_library_log_detail_level(EXTENDED)
set_library_log_hide_sensitive_data(False)

server = Server('my_fake_server')

schema = AddEntryRequestSchema()


def test_add_with_valid_data():
    logging.info('Starting test_add_with_valid_data')

    connection = Connection(server, user='cn=my_user,ou=test,o=lab', password='my_password', client_strategy=MOCK_SYNC)
    connection.bind()

    dn = 'cn=employees,ou=test,o=lab'
    connection.add(dn, 'organizationalUnit')
    result_description = connection.result["description"]
    assert result_description == 'success', f'Add {dn} failed.{result_description}'
    assert connection.last_error is None, f'An error occurred adding {dn}.{connection.last_error}'

    dn = 'cn=users,cn=employees,ou=test,o=lab'
    connection.add(dn, 'organizationalUnit')
    assert result_description == 'success', f'Add {dn} failed.{result_description}'
    assert connection.last_error is None, f'An error occurred adding {dn}.{connection.last_error}'

    dn = 'cn=user0,cn=users,cn=employees,ou=test,o=lab'

    connection.add(dn, 'inetOrgPerson',
                                           {
                                               'userPassword': 'test0000',
                                               'sn': 'user0_sn'})
    assert result_description == 'success', f'Add {dn} failed.{result_description}'
    assert connection.last_error is None, f'An error occurred adding {dn}.{connection.last_error}'

    print(f'Starting search for {dn}')
    # result = connection.search(search_base=dn,
    #                            search_filter='(objectClass=inetOrgPerson)',
    #                            search_scope=BASE,
    #                            attributes=ALL_ATTRIBUTES)
    result = connection.search(search_base='ou=test,o=lab',
                               search_filter='(objectClass=*)',
                               search_scope=SUBTREE,
                               attributes=ALL_ATTRIBUTES)
    print(f'Search {dn} connection.result: {connection.result}')
    print(f'Search {dn} connection.response: {connection.response}')
    print(f'Search {dn} connection.entries: {connection.entries}')
    print(f'Search {dn} connection.last_error: {connection.last_error}')
    print(f'Search {dn} connection.bound: {connection.bound}')
    print(f'Search {dn} connection.listening: {connection.listening}')
    print(f'Search {dn} connection.closed: {connection.closed}')
    assert False

    dn = 'cn=user1,cn=users,cn=employees,ou=test,o=lab'
    print(f'Adding {dn}')
    result = connection.strategy.add_entry(dn, 'inetOrgPerson',
                                           {
                                               'userPassword': 'test0000',
                                               'sn': 'user1_sn'})
    print(f'Add {dn} connection.result: {connection.result}')
    print(f'Add {dn} connection.response: {connection.response}')
    print(f'Add {dn} connection.last_error: {connection.last_error}')
    print(f'Add {dn} connection.bound: {connection.bound}')
    print(f'Add {dn} connection.listening: {connection.listening}')
    print(f'Add {dn} connection.closed: {connection.closed}')
    assert result

    print(f'Starting search for {dn}')
    result = connection.search(search_base=dn,
                               search_filter='(objectClass=inetOrgPerson)', search_scope=BASE,
                               attributes=ALL_ATTRIBUTES)
    print(f'Search {dn} connection.result: {connection.result}')
    print(f'Search {dn} connection.response: {connection.response}')
    print(f'Search {dn} connection.entries: {connection.entries}')
    print(f'Search {dn} connection.last_error: {connection.last_error}')
    print(f'Search {dn} connection.bound: {connection.bound}')
    print(f'Search {dn} connection.listening: {connection.listening}')
    print(f'Search {dn} connection.closed: {connection.closed}')
    assert result

    dn = 'cn=user2,cn=users,cn=employees,ou=test,o=lab'
    print(f'Adding {dn}')
    result = connection.strategy.add_entry(dn, 'inetOrgPerson',
                                           {
                                               'userPassword': 'test0000',
                                               'sn': 'user2_sn'})
    print(f'Add {dn} connection.result: {connection.result}')
    print(f'Add {dn} connection.response: {connection.response}')
    print(f'Add {dn} connection.entries: {connection.entries}')
    print(f'Add {dn} connection.last_error: {connection.last_error}')
    print(f'Add {dn} connection.bound: {connection.bound}')
    print(f'Add {dn} connection.listening: {connection.listening}')
    print(f'Add {dn} connection.closed: {connection.closed}')
    assert result

    print(f'Starting search for {dn}')
    result = connection.search(search_base=dn,
                               search_filter='(objectClass=inetOrgPerson)', search_scope=BASE,
                               attributes=ALL_ATTRIBUTES)
    print(f'Search {dn} connection.result: {connection.result}')
    print(f'Search {dn} connection.response: {connection.response}')
    print(f'Search {dn} connection.entries: {connection.entries}')
    print(f'Search {dn} connection.last_error: {connection.last_error}')
    print(f'Search {dn} connection.bound: {connection.bound}')
    print(f'Search {dn} connection.listening: {connection.listening}')
    print(f'Search {dn} connection.closed: {connection.closed}')
    assert result

    data = {
        'basedn': 'ou=test,o=lab',
        'dn': 'cn=mwatkins,cn=users,cn=employees,ou=test,o=lab',
        # 'object_class': 'top,person,organizationalPerson,inetOrgPerson',
        'object_class': 'inetOrgPerson',
        'attributes': {
            'o': 'lab',
            'ou': 'test'
        }
    }

    controller = LdapController()
    add_entry_request = schema.load(data)
    result = controller.add_entry(connection, add_entry_request)
    print(f'Add {dn} connection.result: {connection.result}')
    print(f'Add {dn} connection.response: {connection.response}')
    print(f'Add {dn} connection.entries: {connection.entries}')
    print(f'Add {dn} connection.last_error: {connection.last_error}')
    print(f'Add {dn} connection.bound: {connection.bound}')
    print(f'Add {dn} connection.listening: {connection.listening}')
    print(f'Add {dn} connection.closed: {connection.closed}')
    assert result
