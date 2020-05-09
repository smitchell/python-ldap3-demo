from flask import jsonify, abort, request, Blueprint

LDAP_API = Blueprint('ldap_api', __name__)


def get_blueprint():
    """Return the blueprint for the main app module"""
    return LDAP_API