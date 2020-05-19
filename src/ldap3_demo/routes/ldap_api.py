#!/usr/bin/env python3
import logging
from typing import Any

from flask import make_response, Response, json, jsonify
from flask import Blueprint
from flask import request
from urllib.parse import unquote
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
    if dn is None:
        return 'Expected query parameter "dn", but found none', 400

    data = {
        'search_base': unquote(dn),
        'search_filter': '(objectClass=*)',
        'search_scope': 'BASE',
        'attributes': 'ALL_ATTRIBUTES'
    }

    search_results = ldap_controller.search(_get_name(request.args), search_schema.load(data))

    return json.dumps(search_results), 200


@ldap_api_blueprint.route('/api/entry/<string:dn>',  methods=['PUT'])
def modify_entry(dn: str):
    if dn is None:
        return 'Expected query parameter "dn", but found none', 400
    content_dn = unquote(dn)
    if content_dn != dn:
        return f'Path dn {dn} does not match content dn {content_dn}', 400

    return jsonify(ldap_controller.modify(_get_name(request.args), search_schema.load(request.data))), 200


@ldap_api_blueprint.route('/api/entry/<string:dn>',  methods=['DELETE'])
def delete_entry(dn: str):
    return jsonify(ldap_controller.delete(_get_name(request.args), unquote(dn))), 205


def _get_name(args) -> str:
    if 'server_name' in args:
        server_name = args['server_name']
    else:
        server_name = 'main'

    return server_name


def _get_dn(args) -> Any:
    if 'dn' not in args:
        return None
    dn = args['dn']
    return unquote(dn)




