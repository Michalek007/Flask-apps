""" Flask application.
    Api views are placed in specific blueprints.
"""
from flask import Flask
import flask_login

from configuration import *


login_manager = flask_login.LoginManager()


def create_app():
    """ Creates Flask application and database object.
        Returns app.
    """
    app = Flask(__name__)
    login_manager.init_app(app)

    # Configuration of app, choose one and uncomment.
    # app.config.from_object(DevelopmentConfig())
    # app.config.from_object(TestingConfig())
    app.config.from_object(ProductionConfig())

    # TODO: implement -> datbase for user authentication and authorisation
    # app.config['db'] = None

    from app.blueprints.auth import auth
    from app.blueprints.config import config
    from app.blueprints.logs import logs
    from app.blueprints.user import user
    from app.blueprints.details import details
    from app.blueprints.hardware import hardware

    app.register_blueprint(auth)
    app.register_blueprint(config)
    app.register_blueprint(logs)
    app.register_blueprint(user)
    app.register_blueprint(details)
    app.register_blueprint(hardware)

    return app
