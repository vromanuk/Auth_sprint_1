import os

from flask import Flask

from src.database.db import init_db
from src.routes import register_blueprints


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    cfg = os.getenv("CONFIG_TYPE", default="src.config.DevelopmentConfig")
    app.config.from_object(cfg)

    register_blueprints(app)
    configure_logging(app)
    init_db()

    return app


def configure_logging(app: Flask):
    import logging
    from logging.handlers import RotatingFileHandler

    from flask.logging import default_handler

    # Deactivate the default flask logger so that log messages don't get duplicated
    app.logger.removeHandler(default_handler)
    file_handler = RotatingFileHandler("flaskapp.log", maxBytes=16384, backupCount=20)
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s [in %(filename)s: %(lineno)d]")
    file_handler.setFormatter(file_formatter)
    app.logger.addHandler(file_handler)
