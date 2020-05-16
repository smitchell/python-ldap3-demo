#!/usr/bin/env python3

from ldap3_demo.dtos.modify_entry_request import ModifyEntryRequest


def test_create_modify_entry_request_dto():
    print('test_create_modify_entry_request_dto')

    changes = {'dn': 'cn=mwatkins,cn=users,cn=employees,ou=test,o=lab',
               'changes': {'mobile': [{'MODIFY_ADD': ['+1 555 555 1862']}]}
               }

    add_entry_request = ModifyEntryRequest('a dn', changes)

    assert add_entry_request.dn == 'a dn'
