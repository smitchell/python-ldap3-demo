#!/usr/bin/env python3

import confuse
from flask import Flask, jsonify, make_response
from flask_swagger_ui import get_swaggerui_blueprint
from .routes import ldap_api

app = Flask(__name__)
config = confuse.Configuration('ldap3_demo', __name__)

### swagger specific ###
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    config['swagger']['ui_url'].get(),
    config['swagger']['api_url'].get(),
    config={
        'app_name': "Python-ldap-demo"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=config['swagger']['ui_url'].get())
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

