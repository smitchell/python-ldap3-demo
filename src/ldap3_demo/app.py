#!/usr/bin/env python3
import logging
import sys
from confuse import Configuration
from flask import Flask, jsonify, make_response
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

config_root = 'ldap3_demo'


def app_register_blueprints(app):
    with app.app_context():
        from .routes import ldap_api
        ### swagger specific ###
        SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
            app.config['swagger']['ui_url'],
            app.config['swagger']['api_url'],
            config={
                'app_name': "Python-ldap-demo"
            }
        )
        app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=app.config['swagger']['ui_url'])
        ### end swagger specific ###
        app.register_blueprint(ldap_api.get_blueprint())


def app_logging_config(app):
    with app.app_context():
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logging.root.addHandler(handler)
        app.logger.setLevel(logging.DEBUG)
        app.logger.addHandler(handler)


def app_init(app):
    CORS(app)
    config = Configuration(config_root, __name__)
    app.config['ldap_servers'] = config['ldap_servers'].get(dict)
    app.config['swagger'] = config['swagger'].get(dict)
    app_register_blueprints(app)


app = Flask(__name__)
app_init(app)
app_logging_config(app)


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
