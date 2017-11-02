from flask import Flask

from app.config import app_config
from .data import db, ma

from app.core.model import * # to trigger migrations

from app.frontend.api.controller import api
from app.frontend.opds.controller import opds
from app.frontend.web.controller import web


def create_app(config_name):

    app = Flask(__name__)

    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(api)
    app.register_blueprint(opds)
    app.register_blueprint(web)

    return app
