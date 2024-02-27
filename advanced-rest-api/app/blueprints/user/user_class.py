from flask import request, jsonify, render_template, current_app
import flask_login
import psutil

from app.blueprints import BlueprintSingleton


class UserClass(BlueprintSingleton):
    """ Implements views related to users. """

    # private methods
    # views
    def protected(self):
        try:
            user_id = flask_login.current_user.id
        except AttributeError:
            return jsonify(logged_user='Anonymous user has no id!')
        return jsonify(logged_user=user_id)

    def logout(self):
        flask_login.logout_user()
        return jsonify(message='Logged out.')

    def logged_users(self):
        users = []
        for user in psutil.users():
            users.append(user.name)
        return jsonify(logged_users=users)

    # gui views
    def users(self):
        return render_template('user/users.html')
