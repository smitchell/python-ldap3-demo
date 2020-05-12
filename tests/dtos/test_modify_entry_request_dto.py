from ldap3_demo.dtos.modify_entry_request import ModifyEntryRequest


def test_create_modify_entry_request_dto():
    print('test_create_modify_entry_request_dto')

    changes = {'phone': [{'MODIFY_ADD': ['9132223344']}]}

    add_entry_request = ModifyEntryRequest('a dn', changes)

    assert add_entry_request.dn == 'a dn'
    assert add_entry_request.changes == changes

