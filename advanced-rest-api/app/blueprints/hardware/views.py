import flask_login

from app.blueprints.hardware import hardware
from app.blueprints.hardware.hardware_class import HardwareClass


@hardware.route('/performance/', methods=['GET'])
@flask_login.login_required
def performance():
    """ Collects computer performance data.
        Output keys: cpu: {usage, freq}, disk: {usage, total, used, free}, virtual_memory: {total, free, available, used}.
    """
    return HardwareClass().performance()


@hardware.route('/stats/', methods=['GET'])
@flask_login.login_required
def stats():
    return HardwareClass().stats()
