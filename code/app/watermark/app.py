import os

from flask import Flask
from flask.ext.bootstrap import Bootstrap

from .config import config


bootstrap = Bootstrap()


def create_app(config_name=None):
    app = Flask(__name__)

    config_name = config_name or os.getenv('CONFIG_ENV') or 'default'
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)

    from . import main
    app.register_blueprint(main)

    return app
