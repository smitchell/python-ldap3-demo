#!/usr/bin/env python3
import logging
from flask import make_response, Response, json, jsonify
from flask import Blueprint
from flask import request
from ldap3_demo.controllers.ldap_controller import LdapController
from ldap3_demo.dtos.add_entry_request import AddEntryRequest
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
    data = request.get_data(as_text=True)
    json_data = json.loads(data)
    logging.info(f'add_entry <-- {json_data}')
    add_entry_request_schema = AddEntryRequestSchema()
    add_entry_request: AddEntryRequest = add_entry_request_schema.load(json_data)
    result: bool = ldap_controller.add(_get_name(request.args), add_entry_request)
    if result:
        logging.warning('add_entry --> 201')
        return 'OK', 201
    logging.warning('add_entry --> 500')
    return 'ERROR', 500


@ldap_api_blueprint.route('/api/entry/<string:dn>',  methods=['GET'])
def get_entry(dn: str):
    data = {
        'search_base': dn,
        'search_filter': '(objectClass=organizationalPerson)',
        'attributes': 'ALL_ATTRIBUTES'
    }

    return jsonify(ldap_controller.search(_get_name(request.ars), search_schema.load(data))), 200


@ldap_api_blueprint.route('/api/entry/<string:dn>',  methods=['PUT'])
def modify_entry(dn: str):
    args = request.args

    if "dn" in args:
        content_dn = args['dn']
        if content_dn != dn:
            return f'Path dn {dn} does not match content dn {content_dn}', 400

    return jsonify(ldap_controller.modify(_get_name(request.args), search_schema.load(request.data))), 200


@ldap_api_blueprint.route('/api/entry/<string:dn>',  methods=['DELETE'])
def delete_entry(dn: str):
    return jsonify(ldap_controller.delete(_get_name(request.args), dn)), 205


def _get_name(args) -> str:
    if 'server_name' in args:
        server_name = args['server_name']
    else:
        server_name = 'main'

    return server_name


