import os
import pathlib

import redis
from flasgger import Swagger
from flask import Flask
from flask_jwt_extended import JWTManager

from src import config, redis_utils
from src.config import SWAGGER_TEMPLATE
from src.database.db import init_db
from src.redis_utils import get_redis
from src.routes import register_blueprints

jwt = JWTManager()
swag = Swagger(template=SWAGGER_TEMPLATE)


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    cfg = os.getenv("CONFIG_TYPE", default="src.config.DevelopmentConfig")
    app.config.from_object(cfg)

    app.config.update({"SWAGGER": {"title": "Auth Service", "openapi": "3.0.3"}})

    register_blueprints(app)
    configure_logging(app)
    # init_db()
    initialize_extensions(app)
    initialize_commands(app)
    setup_redis(app)

    return app


def initialize_extensions(app) -> None:
    jwt.init_app(app)
    swag.init_app(app)


def initialize_commands(app) -> None:
    from src.commands.roles import create_roles
    from src.commands.superuser import create_superuser

    app.cli.add_command(create_superuser)
    app.cli.add_command(create_roles)


def configure_logging(app: Flask) -> None:
    import logging
    from logging.handlers import RotatingFileHandler

    from flask.logging import default_handler

    basedir = pathlib.Path(__file__).parent
    logdir = basedir.joinpath("logs")
    if not logdir.exists():
        logdir.mkdir()
    logfile = logdir.joinpath("flaskapp.log")

    # Deactivate the default flask logger so that log messages don't get duplicated
    app.logger.removeHandler(default_handler)
    file_handler = RotatingFileHandler(logfile, maxBytes=16384, backupCount=20)
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter(
        "%(asctime)s %(levelname)s: %(message)s [in %(filename)s: %(lineno)d]"
    )
    file_handler.setFormatter(file_formatter)
    app.logger.addHandler(file_handler)


def setup_redis(app) -> None:
    redis_utils.redis = redis.StrictRedis(
        host=app.config["REDIS_HOST"],
        port=app.config["REDIS_PORT"],
        db=0,
        decode_responses=True,
    )


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    jwt_redis_blocklist = get_redis()

    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None
