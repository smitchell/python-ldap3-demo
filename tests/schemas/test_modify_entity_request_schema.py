#!/usr/bin/env python3

from ldap3_demo.schemas.modify_entry_request_schema import ModifyEntryRequestSchema

schema = ModifyEntryRequestSchema()

changeEntityRequestJson = {'dn': 'cn=mwatkins,cn=users,cn=employees,ou=test,o=lab',
                           'changes': {'mobile': [{'MODIFY_ADD': ['+1 555 555 1862']}]}
                           }


def test_modify_entry_request_load():
    print('test_modify_entry_request_load')

    modify_entry_request = schema.load(changeEntityRequestJson)

    assert modify_entry_request.dn == changeEntityRequestJson['dn']
    changes = modify_entry_request.changes
    for attribute_key in changes:
        attribute = changes[attribute_key]
        for operation in attribute:
            operation_type = type(operation)
            assert operation_type == tuple, f'Expected class tuple but found {type(operation)}'
