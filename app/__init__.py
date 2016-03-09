import os
from flask import Flask
from flask.ext.marshmallow import Marshmallow
from flask.ext.sqlalchemy import SQLAlchemy

from config import config


db = SQLAlchemy()
ma = Marshmallow()
basedir = os.path.abspath(os.path.dirname(__file__))


def create_app(config_name):
    static_path = os.path.join(basedir, '../static')
    app = Flask(__name__, static_url_path='', static_folder=static_path)
    app.config.from_object(config[config_name])

    db.init_app(app)
    ma.init_app(app)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='')

    return app
