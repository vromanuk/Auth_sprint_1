import os
import pathlib

from flask import Flask
from flask_apispec import FlaskApiSpec
from flask_jwt_extended import JWTManager

from src.database.db import init_db
from src.routes import register_blueprints, swagger_init

jwt = JWTManager()
docs = FlaskApiSpec()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    cfg = os.getenv("CONFIG_TYPE", default="src.config.DevelopmentConfig")
    app.config.from_object(cfg)

    register_blueprints(app)
    configure_logging(app)
    init_db()
    initialize_extensions(app)
    initialize_commands(app)

    return app


def initialize_extensions(app):
    jwt.init_app(app)
    docs.init_app(app)
    swagger_init(docs)


def initialize_commands(app):
    from src.commands.roles import create_roles
    from src.commands.superuser import create_superuser

    app.cli.add_command(create_superuser)
    app.cli.add_command(create_roles)


def configure_logging(app: Flask):
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
