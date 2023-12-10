import flask_login

from app.blueprints.user import user
from app.blueprints.user.user_class import UserClass


@user.route('/protected/')
@flask_login.login_required
def protected():
    """ Returns currently logged users in service.
        Output keys: logged_user.
    """
    return UserClass().protected()


@user.route('/logout/')
@flask_login.login_required
def logout():
    """ Allows to log out from application. """
    return UserClass().logout()


@user.route('/logged_users/', methods=['GET'])
@flask_login.login_required
def logged_users():
    """ Returns list of currently logged users.
        Output keys: logged_users.
    """
    return UserClass().logged_users()


@user.route('/users/')
@flask_login.login_required
def users():
    return UserClass().users()
