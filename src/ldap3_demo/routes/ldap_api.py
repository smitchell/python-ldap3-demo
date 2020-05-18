#!/usr/bin/env python3

from flask import make_response
from flask import Blueprint
from flask import request
from flask import jsonify

from ldap3_demo.controllers.ldap_controller import LdapController
from ldap3_demo.schemas.add_entry_request_schema import AddEntryRequestSchema
from ldap3_demo.schemas.search_schema import SearchSchema

ldap_api_blueprint = Blueprint('ldap_api', __name__)
ldap_controller = LdapController()
search_schema = SearchSchema()


def get_blueprint():
    """Return the blueprint for the main app module"""
    return ldap_api_blueprint


@ldap_api_blueprint.route('/api/entries', methods=['POST'])
def add_entry():
    if not request.is_json:
        return make_response("Login must contain JSON", 400)

    add_entry_request_schema = AddEntryRequestSchema()
    return jsonify(ldap_controller.add(_get_name(request), add_entry_request_schema.load(request.data)))


@ldap_api_blueprint.route('/api/entry/<string:dn>',  methods=['GET'])
def get_entry(dn: str):
    data = {
        'search_base': dn,
        'search_filter': '(objectClass=organizationalPerson)',
        'attributes': 'ALL_ATTRIBUTES'
    }

    return jsonify(ldap_controller.search(_get_name(request), search_schema.load(data)))


@ldap_api_blueprint.route('/api/entry/<string:dn>',  methods=['PUT'])
def modify_entry(dn: str):
    args = request.args

    if "dn" in args:
        content_dn = args['dn']
        if content_dn != dn:
            return make_response(f'Path dn {dn} does not match content dn {content_dn}', 400)

    return jsonify(ldap_controller.modify(_get_name(request), search_schema.load(request.data)))


@ldap_api_blueprint.route('/api/entry/<string:dn>',  methods=['DELETE'])
def delete_entry(dn: str):
    return jsonify(ldap_controller.delete(_get_name(request), dn))


def _get_name(request) -> str:
    args = request.args
    if "server_name" in args:
        server_name = args['server']
    else:
        server_name = 'main'
    return server_name

