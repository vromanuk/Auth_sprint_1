from flask import Blueprint, Flask
from flask_apispec import FlaskApiSpec
from flask_restful import Api

from src.resources.auth import AuthLogin, AuthRegister
from src.resources.smoke import Smoke


def register_blueprints(app: Flask) -> None:
    api_bp = Blueprint("api", __name__, url_prefix="/api/v1")
    api = Api(api_bp)

    api.add_resource(Smoke, "/smoke", strict_slashes=False)
    api.add_resource(AuthRegister, "/register", strict_slashes=False)
    api.add_resource(AuthLogin, "/login", strict_slashes=False)

    app.register_blueprint(api_bp)


def swagger_init(docs: FlaskApiSpec):
    docs.register(Smoke, endpoint="api.smoke")
    docs.register(AuthRegister, endpoint="api.authregister")
    docs.register(AuthLogin, endpoint="api.authlogin")
