import os

from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    cfg = os.getenv("CONFIG_TYPE", default="src.config.DevelopmentConfig")
    app.config.from_object(cfg)

    register_blueprints(app)
    configure_logging(app)

    return app


def register_blueprints(app: Flask):
    from src.resources.smoke import smoke_bp

    app.register_blueprint(smoke_bp)


def configure_logging(app: Flask):
    import logging
    from logging.handlers import RotatingFileHandler

    from flask.logging import default_handler

    # Deactivate the default flask logger so that log messages don't get duplicated
    app.logger.removeHandler(default_handler)

    # Create a file handler object
    file_handler = RotatingFileHandler("flaskapp.log", maxBytes=16384, backupCount=20)

    # Set the logging level of the file handler object so that it logs INFO and up
    file_handler.setLevel(logging.INFO)

    # Create a file formatter object
    file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s [in %(filename)s: %(lineno)d]")

    # Apply the file formatter object to the file handler object
    file_handler.setFormatter(file_formatter)

    # Add file handler object to the logger
    app.logger.addHandler(file_handler)
