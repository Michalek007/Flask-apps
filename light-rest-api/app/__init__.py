""" Flask application.
    Api views are placed in specific blueprints.
"""
from flask import Flask
import flask_login
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt

from configuration import *
from database import create_db_object

login_manager = flask_login.LoginManager()

app = Flask(__name__)
login_manager.init_app(app)

# Configuration of app, choose one and uncomment.
# app.config.from_object(DevelopmentConfig())
# app.config.from_object(TestingConfig())
app.config.from_object(ProductionConfig())

db = create_db_object()
db.init_app(app)
app.config['db'] = db

ma = Marshmallow(app)
app.config['ma'] = ma

bcrypt = Bcrypt(app)
app.config['bcrypt'] = bcrypt

from app.cli import db_create, db_drop, db_init, db_seed_users, db_seed_params


def deploy_app_views():
    """ Deploys app views. Should be called before running app. """
    from app.blueprints.auth import auth
    from app.blueprints.params import params
    from app.blueprints.user import user
    from app.blueprints.config import config
    from app.blueprints.details import details

    app.register_blueprint(auth)
    app.register_blueprint(params)
    app.register_blueprint(user)
    app.register_blueprint(config)
    app.register_blueprint(details)

    from app.views import base
    print("App views deployed!")
