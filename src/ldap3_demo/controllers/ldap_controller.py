from flask import Response
from ldap3 import Server, Connection, ALL

from ldap3_demo.dtos.add_entry_request import AddEntryRequest
from ldap3_demo.schemas.add_entry_request_schema import AddEntryRequestSchema


class LdapController:

    # This method adds a new entry to LDAP. The dn must be unique and must match the dn
    # attribute in the AddEntryRequest.
    def add_entry(self, connection: Connection, add_entry_request: AddEntryRequest):
        schema = AddEntryRequestSchema()
        # exists = connection.search(add_entry_request.basedn, f'(dn={add_entry_request.dn})', 'SUBTREE', 'DEREF_NEVER', 'dn')
        # if exists is not None:
        #     return Response(status=400)

        result = connection.add(add_entry_request.dn, schema.dump(add_entry_request))
        print(result)
        return result


