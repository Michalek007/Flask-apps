from flask import request, jsonify, render_template, current_app

from app.blueprints import BlueprintSingleton
from app.blueprints.config.modules import ClientStatus
from utils import SubprocessApi, ProcessUtil
from configuration import Pid


class ConfigClass(BlueprintSingleton):
    """ Implements views related to service configuration.
        Attributes:
            subprocess: SubprocessApi instance
            process_util: ProcessUtil instance
    """
    subprocess = SubprocessApi()
    process_util = ProcessUtil()

    # private methods
    def kill_dm(self):
        self.process_util.task_kill(pid=Pid.SERVICE)
        self.process_util.task_kill(pid=Pid.CLIENT)

    # views
    def get_pid(self):
        if Pid.CLIENT is not None:
            if not self.process_util.find_process(Pid.CLIENT):
                Pid.CLIENT = None
        return jsonify(SERVICE=Pid.SERVICE, CLIENT=Pid.CLIENT)

    def set_pid(self):
        client_pid = request.args.get('client')
        if client_pid is None:
            return jsonify(message='Wrong key or value was not provided. Expected key: \'client\''), 400
        try:
            client_pid = int(client_pid)
        except (TypeError, ValueError):
            return jsonify(message='PID must be an integer.'), 422
        Pid.CLIENT = client_pid
        return jsonify(message='PID updated successfully.')

    def kill(self):
        self.kill_dm()
        return jsonify(message='Service is shut down!')

    def restart(self):
        self.kill_dm()
        restart_script = f'"{current_app.config.get("RESTART_SCRIPT")}"'
        run_file = f'"{current_app.config.get("RUN_FILE")}"'
        self.subprocess.run(f'start {restart_script} {run_file}', stdout=None, stderr=None)
        return jsonify(message='Service is restarting!')

    def kill_client(self):
        stdout, stderr = self.process_util.task_kill(pid=Pid.CLIENT, capture_output=True)
        if stderr is not None:
            return jsonify(message=stderr[0]), 404  # expected message: "ERROR: The process "None"/<pid> not found."
        Pid.CLIENT = None
        return jsonify(message='Client is shut down!')

    def restart_client(self):
        self.process_util.task_kill(pid=Pid.CLIENT)
        executable = current_app.config.get("EXECUTABLE")
        client_run_file = current_app.config.get("CLIENT_RUN_FILE")
        self.subprocess.run(f'{executable} {client_run_file}', stdout=None, stderr=None)
        return jsonify(message='Client is restarting!')

    def set_client_status(self):
        status = request.args.get('status')
        if status is None:
            return jsonify(message='Wrong key or value was not provided. Expected key: \'status\''), 400
        client_status = ClientStatus()
        client_status.set(status=status)
        return jsonify(message='Client status set successfully.')

    def get_client_status(self):
        client_status = ClientStatus()
        return jsonify(status=client_status.get())

    # gui views
    def settings(self):
        return render_template('config/settings.html')
