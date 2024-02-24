from flask import request, url_for, redirect, render_template, jsonify, current_app
from datetime import datetime

from app.blueprints import BlueprintSingleton
from database.schemas import acceleration_schema, acceleration_many_schema, Acceleration
from utils import DateUtil


class AccBp(BlueprintSingleton):
    """ Implementation of CRUD functionalities for acc (acceleration table).
        Attributes:
            date_util: DateUtil object
    """
    date_util = DateUtil(
        date_format='%Y-%m-%d %H:%M:%S.%f',
        optional_date_format=('%Y-%m-%d %H:%M:%S', '%Y-%m-%d')
    )

    def get_acc_data_from_request(self):
        x_axis = request.args.get('X')
        y_axis = request.args.get('Y')
        z_axis = request.args.get('Z')
        if x_axis is None or y_axis is None or z_axis is None:
            return jsonify(message='Missing value. Expected args: X, Y, Z'), 400
        else:
            return x_axis, y_axis, z_axis

    # views
    def acc(self, acc_id: int = None):
        if acc_id is None:
            timestamp = request.args.get('Timestamp')
            acc_obj = Acceleration.query.all()

            if timestamp is None:
                return jsonify(acc=acceleration_many_schema.dump(acc_obj))

            timestamp = self.date_util.from_string(timestamp)
            if timestamp is None:
                return jsonify(message='Wrong date format. Expected: %Y-%m-%d %H:%M:%S or %Y-%m-%d')

            later_acc = filter(
                lambda item: self.date_util.from_string(item.timestamp) > timestamp, acc_obj
            )
            return jsonify(acc=acceleration_many_schema.dump(later_acc))

        acc_obj = Acceleration.query.filter_by(id=acc_id).first()
        if acc_obj:
            return jsonify(acc=acceleration_schema.dump(acc_obj))
        else:
            return jsonify(message='There are no acc with that id'), 404

    def add_acc(self):
        response = self.get_acc_data_from_request()
        if len(response) < 3:
            return response
        else:
            x_axis, y_axis, z_axis = response

        timestamp = datetime.now()
        acc_obj = Acceleration(
            timestamp=timestamp,
            x_axis=x_axis,
            y_axis=y_axis,
            z_axis=z_axis
        )
        current_app.config.get('db').session.add(acc_obj)
        current_app.config.get('db').session.commit()
        return jsonify(message='Added new acc from ' + acc_obj.timestamp), 202

    def delete_acc(self, acc_id: int = None):
        if acc_id is None:
            timestamp = request.args.get('Timestamp')
            if timestamp is None:
                return jsonify(message='Missing value. Expected arg: Timestamp'), 400

            acc_obj = Acceleration.query.all()
            timestamp = self.date_util.from_string(timestamp)
            if timestamp is None:
                return jsonify(message='Wrong date format. Expected: %Y-%m-%d %H:%M:%S or %Y-%m-%d')
            earlier_acc = filter(
                lambda item: self.date_util.from_string(item.timestamp) < timestamp, acc_obj
            )

            earlier_acc = list(earlier_acc)
            for param in earlier_acc:
                current_app.config.get('db').session.delete(param)
            current_app.config.get('db').session.commit()

            deleted_count = len(earlier_acc)
            if deleted_count == 0:
                return jsonify(message=f'No acc were deleted. '), 404
            return jsonify(message=f'{deleted_count} acc deleted successfully'), 202

        acc_obj = Acceleration.query.filter_by(id=acc_id).first()
        if acc_obj:
            current_app.config.get('db').session.delete(acc_obj)
            current_app.config.get('db').session.commit()
            return jsonify(message='Deleted acc from ' + acc_obj.timestamp), 202
        else:
            return jsonify(message='There are no acc with that id'), 404

    def update_acc(self, acc_id: int = None):
        if acc_id is None:
            return jsonify(message='There is no note with that id'), 404

        response = self.get_acc_data_from_request()
        if len(response) < 3:
            return response
        else:
            x_axis, y_axis, z_axis = response

        acc_obj = Acceleration.query.filter_by(id=acc_id).first()
        if acc_obj:
            acc_obj.x_axis = x_axis
            acc_obj.y_axis = y_axis
            acc_obj.z_axis = z_axis
            current_app.config.get('db').session.commit()
            return jsonify(message='Updated acc from ' + acc_obj.timestamp), 202
        else:
            return jsonify(message='There are no acc with that id'), 404

    # gui views
    def acc_table(self):
        return render_template('acc/acc_table.html')
