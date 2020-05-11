from flask import Flask, jsonify, make_response
from flask_swagger_ui import get_swaggerui_blueprint
from .routes import ldap_api
import logging.config
import json
import os

APP = Flask(__name__)

logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../../logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)

config_json_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../..//config.json'))

with open(config_json_path, "r") as json_file:
    cfg = json.load(json_file)

### swagger specific ###
swagger = cfg['swagger']
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    swagger['url'],
    swagger['api_url'],
    config={
        'app_name': "Python-ldap-demo"
    }
)
APP.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=swagger['url'])
### end swagger specific ###

APP.register_blueprint(ldap_api.get_blueprint())


@APP.errorhandler(400)
def handle_400_error(_error):
    """Return a http 400 error to client"""
    return make_response(jsonify({'error': 'Misunderstood'}), 400)


@APP.errorhandler(401)
def handle_401_error(_error):
    """Return a http 401 error to client"""
    return make_response(jsonify({'error': 'Unauthorised'}), 401)


@APP.errorhandler(404)
def handle_404_error(_error):
    """Return a http 404 error to client"""
    return make_response(jsonify({'error': 'Not found'}), 404)


@APP.errorhandler(500)
def handle_500_error(_error):
    """Return a http 500 error to client"""
    return make_response(jsonify({'error': 'Server error'}), 500)

