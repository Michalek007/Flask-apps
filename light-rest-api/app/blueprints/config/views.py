from flask import request, url_for, redirect, render_template, jsonify, current_app
import flask_login

from app.blueprints.config import config
from configuration import Pid
from utils import ProcessUtil, SubprocessApi


@config.route('/get_pid/', methods=['GET'])
def get_pid():
    """ Returns process pid of service.
        Output keys: SERVICE.
    """
    return jsonify(SERVICE=Pid.SERVICE)


@config.route('/kill/', methods=['GET'])
def kill():
    """ Shuts down service. For development purposes. """
    process_util = ProcessUtil()
    process_util.task_kill(pid=Pid.SERVICE)
    return jsonify(message='Service is shut down!')


@config.route('/restart/', methods=['GET'])
def restart():
    """ Restarts service. For development purposes. """
    process_util = ProcessUtil()
    subprocess = SubprocessApi()

    process_util.task_kill(pid=Pid.SERVICE)
    restart_script = f'"{current_app.config.get("BASEDIR")}\\scripts\\restartService.bat"'
    run_file = f'"{current_app.config.get("BASEDIR")}\\run.bat"'
    subprocess.run(f'start {restart_script} {run_file}', stdout=None, stderr=None)

    return jsonify(message='Service is restarting!')


@config.route('/settings/')
def settings():
    return render_template('config/settings.html')
