from ldap3_demo.schemas.modify_entry_request_schema import ModifyEntryRequestSchema

schema = ModifyEntryRequestSchema()

data = {
    'dn': 'cn=mwatkins,ou=employees,ou=finance,dc=acme,dc=com',
    'changes': {
        'phone': [
            {'MODIFY_ADD': ['913-222-3344']}
        ]
    }
}


def test_modify_entry_request_load():
    print('test_modify_entry_request_load')

    change = schema.load(data)

    assert change.dn == data['dn']
    assert change.changes == data['changes']


def test_modify_entry_request_dump():
    print('test_modify_entry_request_dump')

    output = schema.dump(schema.load(data))

    assert output is not None
    assert output['dn'] == data['dn']
    assert output['changes'] == data['changes']
