
from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
# from routes import ldap_api

APP = Flask(__name__)

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Python-ldap-demo"
    }
)
APP.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###

# APP.register_blueprint(ldap_api.get_blueprint())


class Microservice:

    @staticmethod
    def run():
        print("Hello World...")
