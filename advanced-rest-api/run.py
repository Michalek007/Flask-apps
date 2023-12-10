""" Runs Flask app on development server.
"""
import os

from app import create_app
from configuration import Pid

Pid.SERVICE = os.getpid()

if __name__ == '__main__':
    app = create_app()
    # app.run(host="0.0.0.0")
    app.run()
