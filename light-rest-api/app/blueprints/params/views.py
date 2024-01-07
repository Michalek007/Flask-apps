from flask import request, url_for, redirect, render_template, jsonify, current_app
import flask_login
from datetime import datetime
import psutil

from app.blueprints.params import params as bp_params
from database.schemas import performance_schema, performances_schema, Performance
from utils import DateUtil


@bp_params.route('/params/<int:params_id>/', methods=['GET'])
@bp_params.route('/params/', methods=['GET'])
def params(params_id: int = None):
    """ Returns params with given id or if not specified list of all params from database.
        If given timestamp, returns list of params with later timestamp.
        Input args: /id/, Timestamp.
        Output keys: performance {id, cpu_usage, disk_usage, memory_usage}.
    """
    if params_id is None:
        timestamp = request.args.get('Timestamp')
        parameters = Performance.query.all()

        if timestamp is None:
            return jsonify(performance=performances_schema.dump(parameters))

        date_util = DateUtil(
            date_format='%Y-%m-%d %H:%M:%S.%f',
            optional_date_format=('%Y-%m-%d %H:%M:%S', '%Y-%m-%d')
        )
        timestamp = date_util.from_string(timestamp)
        if timestamp is None:
            return jsonify(message='Wrong date format. Expected: %Y-%m-%d %H:%M:%S or %Y-%m-%d')

        later_params = filter(
            lambda item: date_util.from_string(item.timestamp) > timestamp, parameters
        )
        return jsonify(performance=performances_schema.dump(later_params))

    parameters = Performance.query.filter_by(id=params_id).first()
    if parameters:
        return jsonify(performance=performance_schema.dump(parameters))
    else:
        return jsonify(message='There are no parameters with that id'), 404


@bp_params.route('/add_params/', methods=['POST'])
def add_params():
    """ POST method.
        Adds params to database.
        Input args: MemoryUsage, CpuUsage, DiskUsage.
    """
    memory_usage = request.args.get('MemoryUsage')
    cpu_usage = request.args.get('CpuUsage')
    disk_usage = request.args.get('DiskUsage')
    if memory_usage is None or cpu_usage is None or disk_usage is None:
        return jsonify(message='Missing value. Expected args: MemoryUsage, CpuUsage, DiskUsage'), 400

    timestamp = datetime.now()
    parameters = Performance(
        timestamp=timestamp,
        memory_usage=memory_usage,
        cpu_usage=cpu_usage,
        disk_usage=disk_usage
    )
    current_app.config.get('db').session.add(parameters)
    current_app.config.get('db').session.commit()
    return jsonify(message='Added new parameters from ' + parameters.timestamp), 202


@bp_params.route('/delete_params/', methods=['DELETE'])
@bp_params.route('/delete_params/<int:params_id>/', methods=['DELETE'])
def delete_params(params_id: int = None):
    """ DELETE method.
        Delete params with given id or if given timestamp, deletes params with earlier timestamp.
        Input args: /id/, Timestamp.
    """
    if params_id is None:
        timestamp = request.args.get('Timestamp')
        if timestamp is None:
            return jsonify(message='Missing value. Expected arg: Timestamp'), 400

        parameters = Performance.query.all()
        date_util = DateUtil(
            date_format='%Y-%m-%d %H:%M:%S.%f',
            optional_date_format=('%Y-%m-%d %H:%M:%S', '%Y-%m-%d')
        )
        timestamp = date_util.from_string(timestamp)
        if timestamp is None:
            return jsonify(message='Wrong date format. Expected: %Y-%m-%d %H:%M:%S or %Y-%m-%d')
        earlier_params = filter(
            lambda item: date_util.from_string(item.timestamp) < timestamp, parameters
        )
        earlier_params = list(earlier_params)
        deleted_count = len(earlier_params)
        for param in earlier_params:
            current_app.config.get('db').session.delete(param)
        current_app.config.get('db').session.commit()
        if deleted_count == 0:
            return jsonify(message=f'No params were deleted. '), 404
        return jsonify(message=f'{deleted_count} params deleted successfully'), 202

    parameters = Performance.query.filter_by(id=params_id).first()
    if parameters:
        current_app.config.get('db').session.delete(parameters)
        current_app.config.get('db').session.commit()
        return jsonify(message='Deleted parameters from ' + parameters.timestamp), 202
    else:
        return jsonify(message='There are no parameters with that id'), 404


@bp_params.route('/update_params/<int:params_id>/', methods=['PUT'])
def update_params(params_id: int = None):
    """ PUT method.
        Updates params with given id.
        Input args: MemoryUsage, CpuUsage, DiskUsage.
    """
    if params_id is None:
        return jsonify(message='There is no note with that id'), 404
    memory_usage = request.args.get('MemoryUsage')
    cpu_usage = request.args.get('CpuUsage')
    disk_usage = request.args.get('DiskUsage')

    if memory_usage is None or cpu_usage is None or disk_usage is None:
        return jsonify(message='Missing value. Expected args: MemoryUsage, CpuUsage, DiskUsage'), 400
    parameters = Performance.query.filter_by(id=params_id).first()
    if parameters:
        parameters.memory_usage = memory_usage
        parameters.cpu_usage = cpu_usage
        parameters.disk_usage = disk_usage
        current_app.config.get('db').session.commit()
        return jsonify(message='Updated parameters from ' + parameters.timestamp), 202
    else:
        return jsonify(message='There are no parameters with that id'), 404


@bp_params.route('/performance/', methods=['GET'])
def performance():
    """ Collects computer performance data.
        Output keys: cpu: {usage, freq}, disk: {usage, total, used, free}, virtual_memory: {total, free, available, used}.
    """
    cpu = dict(
        usage=psutil.cpu_percent(0.5),
        freq=psutil.cpu_freq()[0]
    )

    disk_stats = psutil.disk_usage('/')
    disk = dict(
        usage=disk_stats[3],
        total=disk_stats[0] / 10 ** 9,
        used=disk_stats[1] / 10 ** 9,
        free=disk_stats[2] / 10 ** 9
    )

    virtual_memory_stats = psutil.virtual_memory()
    virtual_memory = dict(
        usage=virtual_memory_stats[2],
        total=virtual_memory_stats[0] / 10 ** 9,
        available=virtual_memory_stats[1] / 10 ** 9,
        used=virtual_memory_stats[3] / 10 ** 9
    )
    return jsonify(
        cpu=cpu,
        disk=disk,
        virtual_memory=virtual_memory
    )


@bp_params.route('/params_table/', methods=['GET'])
def params_table():
    return render_template('params/params_table.html')


@bp_params.route('/stats/', methods=['GET'])
def stats():
    return render_template("params/stats.html")
