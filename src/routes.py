from flask import Blueprint, Flask
from flask_apispec import FlaskApiSpec
from flask_restful import Api

from src.resources.auth import AuthLogin, AuthRegister
from src.resources.jwt import TokenRefresh
from src.resources.log_history import LogHistoryResource
from src.resources.smoke import Smoke
from src.resources.users import Users


def register_blueprints(app: Flask) -> None:
    api_bp = Blueprint("api", __name__, url_prefix="/api/v1")
    api = Api(api_bp)

    # Auth
    api.add_resource(AuthRegister, "/register", strict_slashes=False)
    api.add_resource(AuthLogin, "/login", strict_slashes=False)

    # LogHistory
    api.add_resource(LogHistoryResource, "/users/log-history", strict_slashes=False)

    # Smoke
    api.add_resource(Smoke, "/smoke", strict_slashes=False)

    # JWT
    api.add_resource(TokenRefresh, "/refresh", strict_slashes=False)

    # Users
    api.add_resource(Users, "/users", strict_slashes=False)

    app.register_blueprint(api_bp)


def swagger_init(docs: FlaskApiSpec):
    docs.register(Smoke, endpoint="api.smoke")
    docs.register(AuthRegister, endpoint="api.authregister")
    docs.register(AuthLogin, endpoint="api.authlogin")
    docs.register(Users, endpoint="api.users")
    docs.register(TokenRefresh, endpoint="api.tokenrefresh")
    docs.register(LogHistoryResource, endpoint="api.loghistoryresource")
