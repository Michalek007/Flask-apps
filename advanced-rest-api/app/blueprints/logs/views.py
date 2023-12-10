import flask_login

from app.blueprints.logs import logs
from app.blueprints.logs.logs_class import LogsClass


@logs.route('/get_logs/<name>/')
@flask_login.login_required
def get_logs(name: str):
    """ Returns list of logs from given file.
        As argument takes name of logs/file (expected names: client, service).
        Input args: /name/.
        Output keys: logs.
    """
    return LogsClass().get_logs(name=name)


@logs.route('/delete_logs/<name>/')
@flask_login.login_required
def delete_logs(name: str):
    """ Delete logs older than given timestamp.
        As argument takes name of logs/file (expected names: client, service).
        Input args: /name/, timestamp.
    """
    return LogsClass().delete_logs(name=name)


@logs.route('/service_logs/')
@flask_login.login_required
def service_logs():
    return LogsClass().service_logs()


@logs.route('/client_logs/')
@flask_login.login_required
def client_logs():
    return LogsClass().client_logs()
