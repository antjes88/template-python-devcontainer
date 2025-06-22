from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager
import secrets
import os
from src.entrypoints.flaskapp.blueprints.example import example
from src.entrypoints.flaskapp.blueprints.authentication import login
from src.utils.env_var_loader import env_var_loader

if os.environ.get("ISINDEVCONTAINER"):
    env_var_loader(".env")

server = Flask(__name__)


class APIConfig:
    API_TITLE = "Example API"
    SECRET_KEY = secrets.token_urlsafe(32)
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/docs"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    API_SPEC_OPTIONS = {
        "components": {
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                }
            }
        },
        "security": [{"bearerAuth": []}],
    }


server.config.from_object(APIConfig)
api = Api(server)
jwt = JWTManager(server)

api.register_blueprint(login)
api.register_blueprint(example)
