from ldap3_demo.controllers.ldap_controller import LdapController
from ldap3_demo.dtos.search import Search
from ldap3_demo.schemas.add_entry_request_schema import AddEntryRequestSchema
from ldap3 import Server, Connection, MOCK_SYNC, ALL_ATTRIBUTES, BASE, Entry

from ldap3_demo.schemas.search_schema import SearchSchema

server = Server('my_fake_server')
schema = AddEntryRequestSchema()


def test_search_ou_by_dn():
    connection = Connection(server, user='cn=my_user,ou=test,o=lab', password='my_password', client_strategy=MOCK_SYNC)
    connection.bind()

    # Pass the new employees data to the controller
    controller = LdapController()
    add_entry_request = schema.load({
        'dn': 'cn=employees,ou=test,o=lab',
        'object_class': 'organizationalUnit'
    })
    result = controller.add(connection, add_entry_request)
    dn = add_entry_request.dn
    assert result, f'There was a problem adding {dn}'

    data = {
        'search_base': dn,
        'search_filter': '(objectClass=organizationalUnit)',
        'search_scope': 'BASE',
        'attributes': 'ALL_ATTRIBUTES',
        'dereference_aliases': 'DEREF_ALWAYS'
    }
    search_schema = SearchSchema()
    search = search_schema.load(data)
    results = controller.search(connection, search)
    assert len(results) == 1, f'Expect one search result but found {len(results)}'
    entry: Entry = results[0]
    print(f'entry = {entry}')
    print(f'TYPE = {type(entry)}')
    assert entry.entry_dn == dn, 'Expected {dn} but found {entry.entry_dn}'
