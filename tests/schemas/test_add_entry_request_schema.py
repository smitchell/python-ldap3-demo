
from ldap3_demo.schemas.add_entry_request_schema import AddEntryRequestSchema

schema = AddEntryRequestSchema()

data = {
    'dn': 'a dn',
    'object_class': 'inetOrgPerson',
    'attributes': [
        {'key': 'dn', 'value': 'a dn'},
        {'key': 'object_class', 'value': 'inetOrgPerson'},
        {'key': 'object_class', 'value': 'user'},
        {'key': 'mail', 'value': 'bob@company.com'},
        {'key': 'first_name', 'value': 'Bob'},
        {'key': 'last_name', 'value': 'Marley'}]
}


def test_add_entry_request_create():
    print('test_add_entry_request_create')

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
