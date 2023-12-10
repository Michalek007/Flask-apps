""" Flask application.
    Api views are placed in specific blueprints.
"""
from flask import Flask
import flask_login


from configuration import *
from database import db
from cli import Cli
from lib_objects import ma, bcrypt

login_manager = flask_login.LoginManager()

app = Flask(__name__)
login_manager.init_app(app)

# Configuration of app, choose one and uncomment.
# app.config.from_object(DevelopmentConfig())
# app.config.from_object(TestingConfig())
app.config.from_object(ProductionConfig())

db.init_app(app)
app.config['db'] = db

ma.init_app(app)
app.config['ma'] = ma

bcrypt.init_app(app)
app.config['bcrypt'] = bcrypt


cli = Cli(app=app, database=db)
cli.init()


def deploy_app_views():
    """ Deploys app views. Should be called before running app. """
    from app.blueprints.auth import auth
    from app.blueprints.params import params
    from app.blueprints.user import user
    from app.blueprints.config import config

    app.register_blueprint(auth)
    app.register_blueprint(params)
    app.register_blueprint(user)
    app.register_blueprint(config)

    from app.views import base
    print("App views deployed!")
