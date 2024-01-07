""" Runs Flask app on development server. """
import os

from app import create_app
from configuration import Pid


if __name__ == '__main__':
    Pid.SERVICE = os.getpid()
    app = create_app()
    # app.run(host="0.0.0.0")
    app.run()
