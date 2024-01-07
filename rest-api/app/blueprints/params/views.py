import flask_login

from app.blueprints.params import params as bp_params
from app.blueprints.params.params_bp import ParamsBp


@bp_params.route('/params/<int:params_id>/', methods=['GET'])
@bp_params.route('/params/', methods=['GET'])
def params(params_id: int = None):
    """ Returns params with given id or if not specified list of all params from database.
        If given timestamp, returns list of params with later timestamp.
        Input args: /id/, Timestamp.
        Output keys: performance {id, cpu_usage, disk_usage, memory_usage}
    """
    return ParamsBp().params(params_id=params_id)


@bp_params.route('/add_params/', methods=['POST'])
def add_params():
    """ POST method.
        Adds params to database.
        Input args: MemoryUsage, CpuUsage, DiskUsage.
    """
    return ParamsBp().add_params()


@bp_params.route('/delete_params/', methods=['DELETE'])
@bp_params.route('/delete_params/<int:params_id>/', methods=['DELETE'])
def delete_params(params_id: int = None):
    """ DELETE method.
        Delete params with given id or if given timestamp, deletes params with earlier timestamp.
        Input args: /id/, Timestamp.
    """
    return ParamsBp().delete_params(params_id=params_id)


@bp_params.route('/update_params/<int:params_id>/', methods=['PUT'])
def update_params(params_id: int = None):
    """ PUT method.
        Updates params with given id.
        Input args: MemoryUsage, CpuUsage, DiskUsage.
    """
    return ParamsBp().update_params(params_id=params_id)


@bp_params.route('/performance/', methods=['GET'])
def performance():
    """ Collects computer performance data.
        Output keys: cpu: {usage, freq}, disk: {usage, total, used, free}, virtual_memory: {total, free, available, used}.
    """
    return ParamsBp().performance()


@bp_params.route('/params_table/', methods=['GET'])
def params_table():
    return ParamsBp().params_table()


@bp_params.route('/stats/', methods=['GET'])
def stats():
    return ParamsBp().stats()
