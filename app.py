from flask import Flask
from flask_cors import CORS

from routes.api import api_routes


def create_app():
    app = Flask(__name__)

    CORS(app)

    api_routes(app)
    return app
