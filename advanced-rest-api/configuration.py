from datetime import timedelta, datetime
from collections import namedtuple
import json
import os
import subprocess


class Config(object):
    """ Configuration base, for all environments.
    """
    DEBUG = False
    TESTING = False
    SCHEDULER_API_ENABLED = True
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
    LISTENER = {
        'host': '127.0.0.1',
        'port': 5000,
    }
    MIN_ACTIVITY_TIME = 15
    SECRET_KEY = '715460b7e65ed5e3686b0bdc'
    TOKEN = 'd424e55ba0854601fcf53532'
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    COMPUTER_NAME = subprocess.Popen('hostname', shell=True, stdout=subprocess.PIPE).stdout.read().decode()
    COMPUTER_NAME = COMPUTER_NAME.replace('\r', '').replace('\n', '')
    CONFIG_FILE = BASEDIR + '\\config.json'
    SERVICE_LOGS_FILE = 'logs\\service_logs.log'
    CLIENT_LOGS_FILE = 'logs\\client_logs.log'
    LOGS_FORMAT = '%(asctime)s %(levelname)s: %(message)s'

    @staticmethod
    def get_project_details():
        """ Returns name-tuple of project details extracted from json config file. """
        with open(Config.CONFIG_FILE, 'r') as f:
            data = json.loads(f.read(), object_hook=lambda args: namedtuple('X', args.keys())(*args.values()))
        return data


class DevelopmentConfig(Config):
    DEBUG = True
    LOGIN_DISABLED = True


class ProductionConfig(Config):
    pass


class TestingConfig(Config):
    TESTING = True
    LOGIN_DISABLED = True


class Pid:
    """ Contains service and client processes pids value. """
    SERVICE = None
    CLIENT = None
