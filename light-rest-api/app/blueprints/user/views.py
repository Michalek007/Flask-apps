from flask import request, url_for, redirect, render_template, jsonify, current_app
import flask_login

from app.blueprints.user import user
from database.schemas import user_schema, users_schema, User


@user.route('/register/', methods=['GET', 'POST'])
def register():
    """ Allows to register new user.
        Input args: login, password, repeat_password
    """
    if request.method == 'GET':
        try:
            test_id = flask_login.current_user.id
        except AttributeError:
            test_id = None
        if test_id is not None:
            return redirect(url_for('auth.logged_in'))
        login = request.args.get('login')
        password = request.args.get('password')
        if not login:
            return render_template('user/register.html')
    else:
        login = request.form.get('login')
        password = request.form.get('password')
        repeat_password = request.form.get('repeat_password')
        if password != repeat_password:
            return jsonify(message='Passwords are not the same!'), 408
        if login is None or password is None:
            return jsonify(
                message='No value. Expected values for keys: \'login\', \'password\', \'repeat_password\''), 400

    test_user = User.query.filter_by(username=login).first()
    if test_user:
        return jsonify(message='That username is already taken!'), 409
    else:
        pw_hash = current_app.config.get('bcrypt').generate_password_hash(password)
        new_user = User(username=login, pw_hash=pw_hash)
        current_app.config.get('db').session.add(new_user)
        current_app.config.get('db').session.commit()
        return jsonify(message='User created successfully.'), 201


@user.route('/logout/', methods=['GET'])
@flask_login.login_required
def logout():
    """ Allows to log out from application. """
    flask_login.logout_user()
    return jsonify(message='Logged out.')


@user.route("/protected/", methods=["GET"])
@flask_login.login_required
def protected():
    """ Returns currently logged users in service.
        Output keys: logged_user.
    """
    try:
        user_id = flask_login.current_user.id
    except AttributeError:
        return jsonify(logged_user="Anonymous user has no id!")
    return jsonify(logged_user=user_id)


@user.route('/users/<int:id>/', methods=['GET'])
@user.route('/users/', methods=['GET'])
def users(id: int = None):
    """ Returns user with given id or if not specified list of all users from database.
        Input args: /id/
        Output keys: Users/User {id, pw_hash, username}
    """
    if id is None:
        users_list = User.query.all()
        return jsonify(users=users_schema.dump(users_list))
    user = User.query.filter_by(id=id).first()
    if user:
        return jsonify(user=user_schema.dump(user))
    else:
        return jsonify(message='There is no user with that id'), 404


@user.route('/users_table/', methods=['GET'])
def users_table():
    return render_template('user/users_table.html')
