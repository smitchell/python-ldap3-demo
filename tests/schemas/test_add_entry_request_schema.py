
from ldap3_demo.schemas.add_entry_request_schema import AddEntryRequestSchema

schema = AddEntryRequestSchema()

data = {
    'dn': 'cn=mwatkins,ou=employees,ou=finance,dc=acme,dc=com',
    'object_class': 'inetOrgPerson,user,supervisor',
    'attributes': {
        'dn': 'a dn',
        'mail': 'bob@company.com',
        'first_name': 'Bob',
        'last_name': 'Marley'}
}


def test_add_entry_request_load():
    print('test_add_entry_request_load')

    add_entry_request = schema.load(data)

    assert add_entry_request.dn == data['dn']
    assert add_entry_request.object_class == data['object_class']


def test_add_entry_request_dump():
    print('test_add_entry_request_dump')

    output = schema.dump(schema.load(data))

    assert output is not None
    assert output['dn'] == data['dn']
    assert output['object_class'] == data['object_class']
    assert output['attributes'] == data['attributes']
