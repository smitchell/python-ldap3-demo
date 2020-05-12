from ldap3_demo.dtos.add_entry_request import AddEntryRequest


def test_create_add_entry_request():
    print('test_create_add_entry_request')

    attributes = {
        'dn': 'cn=mwatkins,ou=employees,ou=finance,dc=acme,dc=com',
        'object_class': 'inetOrgPerson,user,supervisor',
        'mail': 'bob@company.com',
        'first_name': 'Bob',
        'last_name': 'Marley'}

    add_entry_request = AddEntryRequest('a dn', 'inetOrgPerson', attributes)

    assert add_entry_request.dn == 'a dn'
    assert add_entry_request.object_class == 'inetOrgPerson'
    assert add_entry_request.attributes == attributes
