from flask import request, url_for, redirect, render_template, jsonify, current_app
import flask_login

from app.blueprints import BlueprintSingleton
from app.blueprints.auth.modules import User


class AuthClass(BlueprintSingleton):
    """ Implements views for user authentication and authorisation.
        Contains login manager methods.
    """

    # private methods
    def validate_user(self, login, password):
        """ Checks if user is valid.
            Args:
                login: user id
                password: user password
            Returns:
                ``None`` if user is valid. otherwise tuple (<message>, <error_code>)
        """
        # TODO: implement -> database user verification
        # verification = current_app.config.get('db').verify_user(login, password)
        verification = True
        if verification:
            test = True
        else:
            return 'Database connection failure', 408
        if test is None:
            return 'There is no account with that login', 401
        if not test:
            return 'Wrong password', 401
        return None

    def has_acces(self, login):
        """ Checks if user has access to service.
            Args:
                login: user id
            Returns:
                ``True`` if user has access, ``False`` otherwise
        """
        # TODO: implement -> database user check privilege
        return True

    def log_user(self, login):
        """ Logs user to service.
            Args:
                login: user id
        """
        user = User()
        user.id = login
        flask_login.login_user(user)

    # login manager methods
    def user_loader(self, login):
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

    def request_loader(self, request):
        auth = request.headers.get('Authorization')
        if not auth:
            return
        token = auth.split()[1]
        if token != current_app.config.get('TOKEN'):
            return
        user = User()
        user.id = token
        return user

    def unauthorized_handler(self):
        return jsonify(message='Unauthorized'), 401

    # views
    def base(self):
        return redirect('login')

    def login(self):
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

        output = self.validate_user(login, password)
        if output is not None:
            return jsonify(message=output[0]), output[1]
        if self.has_acces(login):
            self.log_user(login)
            if request.method == "POST":
                return redirect(url_for('auth.logged_in'))
            return redirect(url_for('user.protected'))

        return jsonify(message='You don\'t have access to this API.'), 401

    # gui views
    def logged_in(self):
        return render_template('auth/logged_in.html')
