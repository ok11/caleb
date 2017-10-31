# app/__init__.py

from app.core.helper import DataEncoder
from flask import Flask

from app.config import app_config
from .database import db

from app.core.model import * # to trigger migrations

from app.frontends.api.controller import api
from app.frontends.opds.controller import opds
from app.frontends.web.controller import web

def create_app(config_name):
    app = Flask(__name__)
    app.json_encoder = DataEncoder
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.register_blueprint(api)
    app.register_blueprint(opds)
    app.register_blueprint(web)

    db.init_app(app)

    return app