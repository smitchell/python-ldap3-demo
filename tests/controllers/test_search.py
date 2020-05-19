#!/usr/bin/env python3
from confuse import Configuration
from ldap3_demo.controllers.connection_manager import ConnectionManager
from ldap3_demo.controllers.ldap_controller import LdapController
from ldap3_demo.schemas.add_entry_request_schema import AddEntryRequestSchema
from ldap3 import Entry

from ldap3_demo.schemas.search_schema import SearchSchema

schema = AddEntryRequestSchema()
config = Configuration('ldap3_demo', __name__)
connection_manager = ConnectionManager(config['ldap'].get(dict))

attributes = {
    'cn': 'Charles Evans, Chuck Evans',
    'dn': 'cn=cevans,cn=users,cn=employees,ou=test,o=lab',
    'o': 'lab',
    'ou': 'test',
    'sn': 'evans',
    'uid': 'cevans',
    'givenName': 'charles',
    'initials': 'CPE',
    'displayName': 'Chuck Evans',
    'telephoneNumber': '+1 408 555 3433',
    'homePhone': '+1 555 555 3532',
    'mobile': '+1 555 555 3375',
    'userPassword': '123password',
    'employeeNumber': 'mpw-6453',
    'employeeType': 'full time',
    'preferredLanguage': 'en-US',
    'mail': 'mwatkins@company.com',
    'title': 'consultant, senior consultant',
    'labeledURI': 'http://www.comapny.com/users/cevans My Home Page'
}


def test_search_ou_by_dn():

    # Pass the new employees data to the controller
    controller = LdapController()
    add_entry_request = schema.load({
        'dn': 'cn=employees,ou=test,o=lab',
        'object_class': 'organizationalUnit'
    })
    result = controller.add(connection_manager.mocked, add_entry_request)
    dn = add_entry_request.dn
    assert result, f'There was a problem adding {dn}'

    data = {
        'search_base': dn,
        'search_filter': '(objectClass=organizationalUnit)',
        'search_scope': 'BASE'
    }
    search_schema = SearchSchema()
    results = controller.search(connection_manager.mocked, search_schema.load(data))
    assert len(results) == 1, f'Expect one search result but found {len(results)}'
    entry = results[0]
    assert entry['dn'] == dn, f'Expected {dn} but found {entry["dn"]}'


def test_search_person_by_dn():

    # Pass the new employees data to the controller
    controller = LdapController()
    add_entry_request = schema.load({
        'dn': 'cn=employees,ou=test,o=lab',
        'object_class': 'organizationalUnit'
    })
    controller.add(connection_manager.mocked, add_entry_request)

    add_entry_request = schema.load({
        'dn': 'cn=users,cn=employees,ou=test,o=lab',
        'object_class': 'organizationalUnit'
    })
    controller.add(connection_manager.mocked, add_entry_request)

    add_entry_request = schema.load({
        'dn': 'cn=cevans,cn=users,cn=employees,ou=test,o=lab',
        'object_class': ['top,person', 'organizationalPerson', 'inetOrgPerson'],
        'attributes': attributes
    })
    controller.add(connection_manager.mocked, add_entry_request)

    data = {
        'search_base': add_entry_request.dn,
        'search_filter': '(objectClass=organizationalPerson)',
        'search_scope': 'BASE'
    }
    search_schema = SearchSchema()
    results = controller.search(connection_manager.mocked, search_schema.load(data))
    assert len(results) == 1, f'Expect one search result but found {len(results)}'
    entry = results[0]
    assert entry['dn'] == add_entry_request.dn, f'Expected {add_entry_request.dn} but found {entry["dn"]}'

