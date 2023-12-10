import flask_login

from app.blueprints.config import config
from app.blueprints.config.config_class import ConfigClass


@config.route('/get_pid/', methods=['GET'])
@flask_login.login_required
def get_pid():
    """ Returns process pid of service and client.
        Output keys: SERVICE, CLIENT.
    """
    return ConfigClass().get_pid()


@config.route('/set_pid/', methods=['POST'])
@flask_login.login_required
def set_pid():
    """ Sets process pid of client.
        Should not be used manually.
    """
    return ConfigClass().set_pid()


@config.route('/kill/', methods=['GET'])
@flask_login.login_required
def kill():
    """ Shuts down server. For development purposes. """
    return ConfigClass().kill()


@config.route('/restart/', methods=['GET'])
@flask_login.login_required
def restart():
    """ Restarts server. For development purposes. """
    return ConfigClass().restart()


@config.route('/kill_client/', methods=['GET'])
@flask_login.login_required
def kill_client():
    """ Shuts down client. For development purposes. """
    return ConfigClass().kill_client()


@config.route('/restart_client/', methods=['GET'])
@flask_login.login_required
def restart_client():
    """ Restarts client. For development purposes. """
    return ConfigClass().restart_client()


@config.route('/set_client_status/', methods=['GET'])
@flask_login.login_required
def set_client_status():
    """ Sets client status.
        Should not be used manually.
    """
    return ConfigClass().set_client_status()


@config.route('/get_client_status/', methods=['GET'])
@flask_login.login_required
def get_client_status():
    """ Returns client status.
        Output keys: status.
    """
    return ConfigClass().get_client_status()


@config.route('/settings/')
@flask_login.login_required
def settings():
    return ConfigClass().settings()
