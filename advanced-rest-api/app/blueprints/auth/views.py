import flask_login

from app.blueprints.auth import auth
from app.blueprints.auth.auth_class import AuthClass
from app.blueprints import login_manager


@login_manager.user_loader
def user_loader(login):
    return AuthClass().user_loader(login)


@login_manager.request_loader
def request_loader(request):
    return AuthClass().request_loader(request)


@login_manager.unauthorized_handler
def unauthorized_handler():
    return AuthClass().unauthorized_handler()


@auth.route('/')
def base():
    return AuthClass().base()


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    """ Allows to log into api.
        Input args: login, password.
        If logging was successful you will be redirected to url:
        GET method -> /protected/
        POST method -> /logged_in/
    """
    return AuthClass().login()


@auth.route('/logged_in/')
@flask_login.login_required
def logged_in():
    return AuthClass().logged_in()
