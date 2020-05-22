#!/usr/bin/env python3
from confuse import Configuration
from ldap3_demo.controllers.connection_manager import ConnectionManager
from ldap3_demo.controllers.ldap_controller import LdapController
from ldap3_demo.schemas.search_schema import SearchSchema
from ldap3_demo.app import config_root

config = Configuration(config_root, __name__)
connection_manager = ConnectionManager(config.get(dict))
controller = LdapController()
search_schema = SearchSchema()


def test_delete_bad_dn():
    assert controller.delete('mocked', "doogie")


def test_delete_good_dn():
    dn = 'cn=random_cn,cn=groups,ou=test,o=lab'
    connection = connection_manager.get_connection('mocked')
    connection.bind()
    connection.add(dn, object_class='organizationalUnit')
    data = {
        'search_base': dn,
        'search_filter': '(objectClass=organizationalUnit)',
        'search_scope': 'BASE',
        'attributes': 'ALL_ATTRIBUTES'
    }

    results: list = controller.search('mocked', search_schema.load(data))
    assert len(results) == 1, f'BEFORE: Expected 1 search result but found {len(results)}'

    assert controller.delete('mocked', dn)

    results: list = controller.search('mocked', search_schema.load(data))
    print(f'AFTER results type --> {type(results)}')
    print(f'AFTER results  --> {results}')
    assert len(results) == 0, f'AFTER: Expected 1 search result but found {results}'

