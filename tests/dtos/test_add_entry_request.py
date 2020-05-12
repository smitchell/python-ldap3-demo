from ldap3_demo.dtos.add_entry_request import AddEntryRequest
from ldap3_demo.dtos.attribute import Attribute


def test_create_add_entry_request():
    print('test_create_add_entry_request')

    attributes = [
        Attribute('dn', 'a dn'),
        Attribute('object_class', 'inetOrgPerson'),
        Attribute('object_class', 'user'),
        Attribute('mail', 'bob@company.com'),
        Attribute('first_name', 'Bob'),
        Attribute('last_name', 'Marley')]

    add_entry_request = AddEntryRequest('a dn', 'inetOrgPerson', attributes)

    assert add_entry_request.dn == 'a dn'
    assert add_entry_request.object_class == 'inetOrgPerson'
    assert add_entry_request.attributes == attributes
