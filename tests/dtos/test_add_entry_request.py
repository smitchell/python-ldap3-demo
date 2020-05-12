from ldap3_demo.dtos.add_entry_request import AddEntryRequest
from ldap3_demo.dtos.key_value_pair import KeyValuePair


def test_create_add_entry_request():
    print('test_create_add_entry_request')

    attributes = [
        KeyValuePair('dn', 'a dn'),
        KeyValuePair('object_class', 'inetOrgPerson'),
        KeyValuePair('object_class', 'user'),
        KeyValuePair('mail', 'bob@company.com'),
        KeyValuePair('first_name', 'Bob'),
        KeyValuePair('last_name', 'Marley')]

    add_entry_request = AddEntryRequest('a dn', 'inetOrgPerson', attributes)

    assert add_entry_request.dn == 'a dn'
    assert add_entry_request.object_class == 'inetOrgPerson'
    assert add_entry_request.attributes == attributes
