#!/usr/bin/env python3
from ldap3_demo.app import connection_manager
from ldap3_demo.controllers.ldap_controller import LdapController


def test_delete_bad_dn():
    controller = LdapController()
    assert controller.delete(connection_manager.mocked, "doogie")


def test_delete_good_dn():
    dn = 'cn=users,cn=groups,ou=test,o=lab'
    connection = connection_manager.get_connection(connection_manager.mocked)
    connection.bind()
    connection.add(dn, object_class='organizationalUnit')

    controller = LdapController()
    assert controller.delete(connection_manager.mocked, dn)

