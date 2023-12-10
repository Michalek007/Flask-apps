""" Database package with factory method -> create_db_object.
    Contains database models & schemas.
    Usage:
        from database import create_db_object
        db = create_db_object()
        db.init_app(app)
"""
from flask_sqlalchemy import SQLAlchemy


def create_db_object():
    """ Returns database SQLAlchemy object. """
    db = SQLAlchemy()
    return db
