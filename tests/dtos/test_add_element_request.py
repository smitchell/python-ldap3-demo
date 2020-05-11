from ldap3_demo.dtos.add_element_request import AddElementRequest
from ldap3_demo.dtos.attribute import Attribute


def test_create_add_element_request():
    print('test_create_add_element_request')

    attributes = [
        Attribute('dn', ['a dn']),
        Attribute('object_class', ['inetOrgPerson']),
        Attribute('object_class', ['user']),
        Attribute('mail', ['bob@company.com']),
        Attribute('first_name', ['Bob']),
        Attribute('last_name', ['Marley'])]

    add_element_request = AddElementRequest('a dn', 'inetOrgPerson', attributes)

    assert add_element_request.dn == 'a dn'
    assert add_element_request.object_class == 'inetOrgPerson'
