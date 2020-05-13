from flask import Response
from ldap3 import Server, Connection, ALL, BASE, ALL_ATTRIBUTES
from marshmallow import pprint

from ldap3_demo.dtos.add_entry_request import AddEntryRequest
from ldap3_demo.schemas.add_entry_request_schema import AddEntryRequestSchema


class LdapController:
    temp = {
        'cn': 'Margaret Watkins, Margie Watkins',
            'displayName': 'Margie Watkins',
            'dn': 'cn=mwatkins,cn=users,cn=employees,ou=test,o=lab',
            'employeeNumber': 'mpw-3948',
            'employeeType': 'full time',
            'givenName': 'Margaret',
            'homePhone': '+1 555 555 1862',
            'initials': 'MPW',
            'labeledURI': 'http://www.comapny.com/users/mwatkins My Home Page',
            'mail': 'mwatkins@company.com',
            'mobile': '+1 555 555 1862',
            'o': 'lab',
            'ou': 'test',
            'preferredLanguage': 'en-US',
            'sn': 'Watkins',
            'telephoneNumber': '+1 408 555 1862',
            'title': 'consultant, senior consultant',
            'uid': 'mwatkins',
            'userPassword': '123password'
            }

    @staticmethod
    def scrub_json(json):
        if 'controls' in json:
            controls = json['controls']
            if controls is None or controls == 'None' or len(controls) == 0:
                del json['controls']
        if 'attributes' in json:
            attributes = json['attributes']
            if attributes is None or attributes == 'None' or len(attributes) == 0:
                del json['attributes']

    # This method adds a new entry to LDAP. The dn must be unique and must match the dn
    # attribute in the AddEntryRequest.
    def add(self, connection: Connection, add_entry_request: AddEntryRequest):
        schema = AddEntryRequestSchema()

        json = schema.dump(add_entry_request)
        LdapController.scrub_json(json)

        if 'controls' in json:
            if 'attributes' in json:
                connection.add(add_entry_request.dn, json['object_class'], json['attributes'], json['controls'])
            else:
                connection.add(add_entry_request.dn, json['object_class'], None, json['controls'])
        elif 'attributes' in json:
            connection.add(add_entry_request.dn, json['object_class'], json['attributes'])
        else:
            # connection.add('cn=employees,ou=test,o=lab', 'organizationalUnit')
            connection.add(add_entry_request.dn, json['object_class'])

        result_description = connection.result["description"]
        if result_description == 'entryAlreadyExists':
            return Response(
                f'The dn {dn} already exists: {connection.last_error}',
                status=400,
            )

        if result_description != 'success':
            return Response(
                f'An error occurred: {connection.last_error}',
                status=500,
            )

        return True
