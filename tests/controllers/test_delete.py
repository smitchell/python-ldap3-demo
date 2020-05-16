#!/usr/bin/env python3

from ldap3 import Server, Connection, MOCK_SYNC

from ldap3_demo.controllers.ldap_controller import LdapController

server = Server('my_fake_server')


def test_delete_bad_dn():
    connection = Connection(server, user='cn=my_user,ou=test,o=lab', password='my_password', client_strategy=MOCK_SYNC)
    connection.bind()

    controller = LdapController()
    assert controller.delete(connection, "doogie")


def test_delete_good_dn():
    connection = Connection(server, user='cn=my_user,ou=test,o=lab', password='my_password', client_strategy=MOCK_SYNC)
    connection.bind()

    dn = 'cn=users,cn=groups,ou=test,o=lab'
    connection.add(dn, object_class='organizationalUnit')

    controller = LdapController()
    assert controller.delete(connection, dn)

