from flask import request, jsonify, render_template, current_app

from app.blueprints import BlueprintSingleton
from app.blueprints.logs.modules import LogsHandler
from utils import DateUtil


class LogsClass(BlueprintSingleton):
    """ Implements views related to logs.
        Attributes:
            date_util: DateUtil instance
            logs_names: available logs files
    """
    date_util = DateUtil(date_format='%Y-%m-%d %H:%M:%S.%f', optional_date_format='%Y-%m-%d %H:%M:%S')
    logs_names = ('client', 'service')

    # private methods
    def is_valid(self, name: str):
        return name in self.logs_names

    # views
    def delete_logs(self, name: str):
        if name not in self.logs_names:
            return jsonify(message='Incorrect name. Expected: "client", "service"'), 422
        timestamp = request.args.get('timestamp')
        if not timestamp:
            return jsonify(message='No value. Expected value for key: \'timestamp\''), 400
        timestamp = self.date_util.from_string(timestamp)
        if timestamp is None:
            return jsonify(message='Wrong date format. Expected: "%Y-%m-%d %H:%M:%S.%f"'), 422
        logs_handler = LogsHandler.get_log_handler(name)
        if logs_handler is None:
            return jsonify(message='File does not exist.'), 404
        logs_handler.delete(timestamp)
        return jsonify(message='Logs deleted successfully.')

    def get_logs(self, name: str):
        if name not in self.logs_names:
            return jsonify(message='Incorrect name. Expected: "client", "service"'), 422
        logs_handler = LogsHandler.get_log_handler(name)
        if logs_handler is None:
            return jsonify(message='File does not exist.'), 404
        logs = logs_handler.get()
        return jsonify(logs=logs)

    # gui views
    def service_logs(self):
        return render_template('logs/service_logs.html')

    def client_logs(self):
        return render_template('logs/client_logs.html')
