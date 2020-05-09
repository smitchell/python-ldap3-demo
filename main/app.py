
from flask import Flask


class Microservice:
    APP = Flask(__name__)

    @staticmethod
    def run():
        print("Hello World...")
