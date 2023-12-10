from flask import request, url_for, redirect, render_template, jsonify, current_app
import flask_login

from app.blueprints.auth import auth
from app.blueprints.auth.modules import User, Authenticator
from app.blueprints import login_manager


@login_manager.user_loader
def user_loader(login):
    # TODO: implement -> database user verification
    # verification = current_app.config.get('db').verify_user(login, 'password')
    verification = True
    test = None
    if verification:
        test = True
    if test is None:
        return
    user = User()
    user.id = login
    return user


@login_manager.request_loader
def request_loader(request):
    auth = request.headers.get('Authorization')
    if not auth:
        return
    token = auth.split()[1]
    if token != current_app.config.get('TOKEN'):
        return
    user = User()
    user.id = token
    return user


@login_manager.unauthorized_handler
def unauthorized_handler():
    return jsonify(message='Unauthorized'), 401


@auth.route('/')
def base():
    return redirect('login')


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    """ Allows to log into service.
        Input args: login, password
        If logging was successful you will be redirected to url:
        GET method -> /protected/
        POST method -> /logged_in/
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
            return render_template('auth/login.html')
    else:
        login = request.form.get('login')
        password = request.form.get('password')
        if login is None or password is None:
            return jsonify(message='No value. Expected values for keys: \'login\', \'password\''), 400
    authenticator = Authenticator(login=login, password=password)
    output = authenticator.validate_user()
    if output is not None:
        return jsonify(message=output[0]), output[1]
    if authenticator.has_acces():
        user = User()
        user.id = login
        flask_login.login_user(user)
        if request.method == "POST":
            return redirect(url_for('auth.logged_in'))
        return redirect(url_for('user.protected'))

    return jsonify(message='You don\'t have access to this API.'), 401


@auth.route('/logged_in/')
@flask_login.login_required
def logged_in():
    return render_template('auth/logged_in.html')
