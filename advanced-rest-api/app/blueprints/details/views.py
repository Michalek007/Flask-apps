import flask_login

from app.blueprints.details import details
from app.blueprints.details.details_class import DetailsClass


@details.route('/app_details/', methods=['GET'])
@flask_login.login_required
def app_details():
    """ Returns project details.
        Output keys: ProjectName, Version, RootDirectory, HostName.
    """
    return DetailsClass().app_details()


@details.route('/help/', methods=['GET'])
@details.route('/help/<method>/', methods=['GET'])
@flask_login.login_required
def help(method=None):
    """ Returns docs for given method or if not specified list of docs for all service methods.
        Input args: /method/.
        Output keys: api_methods: {<method_name>} or <method_name>.
    """
    return DetailsClass().help(method=method)


@details.route('/info/')
@flask_login.login_required
def info():
    return DetailsClass().info()


@details.route('/methods/')
@flask_login.login_required
def methods():
    return DetailsClass().methods()
