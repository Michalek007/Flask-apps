""" Deploys Flask app as wsgi server. """
import sys
from gevent.monkey import patch_all; patch_all()
from gevent import pywsgi
import logging
import os
from pathlib import Path

from app import create_app
from configuration import Pid, Config


if sys.executable != str(Path(Config.BASEDIR + '/.venv/Scripts/python.exe')):
    sys.stdout = sys.stderr = open(os.devnull, 'w')

app = create_app()
app.config.update({'EXECUTABLE': sys.executable})
if sys.executable == str(Path(Config.BASEDIR + '/.venv/Scripts/python.exe')):
    app.config.update({'RUN_FILE': Path(Config.BASEDIR + '/run.bat')})

server_wsgi = pywsgi.WSGIServer(listener=('0.0.0.0', Config.LISTENER['port']), application=app)


class StreamToLogger(object):
    """ Fake file-like stream object that redirects writes to a logger instance. """

    def __init__(self, logger, log_level=logging.ERROR):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

    def flush(self):
        pass


def run(server: pywsgi.WSGIServer):
    """ Configures logger and starts server. """
    logging.basicConfig(format=Config.LOGS_FORMAT, filename=Config.SERVICE_LOGS_FILE)

    stdout_logger = logging.getLogger('STDOUT')
    sl = StreamToLogger(stdout_logger, logging.INFO)
    sys.stdout = sl

    stderr_logger = logging.getLogger('STDERR')
    sl = StreamToLogger(stderr_logger, logging.ERROR)
    sys.stderr = sl
    return server.serve_forever()


if __name__ == '__main__':
    Pid.SERVICE = os.getpid()
    run(server_wsgi)
