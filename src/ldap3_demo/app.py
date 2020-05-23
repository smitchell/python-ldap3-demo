#!/usr/bin/env python3
import logging
import sys

from confuse import Configuration
from flask import Flask, jsonify, make_response
from flask_swagger_ui import get_swaggerui_blueprint
from .routes import ldap_api
from flask_cors import CORS

config_root = 'ldap3_demo'

app = Flask(__name__)


with app.app_context():
    CORS(app)
    config = Configuration(config_root, __name__)
    app.config['ldap_servers'] = config['ldap_servers'].get()
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logging.root.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)

    ### swagger specific ###
    SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
        config['swagger']['ui_url'].get(str),
        config['swagger']['api_url'].get(str),
        config={
            'app_name': "Python-ldap-demo"
        }
    )
    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=config['swagger']['ui_url'].get(str))
    ### end swagger specific ###

    app.register_blueprint(ldap_api.get_blueprint())


@app.errorhandler(400)
def handle_400_error(_error):
    """Return a http 400 error to client"""
    return make_response(jsonify({'error': 'Misunderstood'}), 400)


@app.errorhandler(401)
def handle_401_error(_error):
    """Return a http 401 error to client"""
    return make_response(jsonify({'error': 'Unauthorised'}), 401)


@app.errorhandler(404)
def handle_404_error(_error):
    """Return a http 404 error to client"""
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(500)
def handle_500_error(_error):
    """Return a http 500 error to client"""
    return make_response(jsonify({'error': 'Server error'}), 500)

