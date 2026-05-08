from flask import Flask
from flask_cors import CORS

from routes.api import api_routes
from routes.frontend import frontend_routes


def create_app():
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
        static_url_path="/",
    )

    CORS(app)

    api_routes(app)
    frontend_routes(app)
    return app
