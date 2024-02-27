""" Runs Flask app on development server. """
import os
import sys
from pathlib import Path

from app import create_app
from configuration import Config, Pid


if __name__ == '__main__':
    Pid.SERVICE = os.getpid()
    app = create_app()
    app.config.update({'EXECUTABLE': sys.executable})
    app.config.update({'RUN_FILE': Path(Config.BASEDIR + '/runDevelopmentServer.bat')})
    # app.run(host='0.0.0.0')
    app.run()
