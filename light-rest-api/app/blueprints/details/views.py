from flask import request, jsonify, render_template, current_app
import flask_login

from app.blueprints.details import details
from app.blueprints.details.modules import ServiceMethods
from configuration import Config


@details.route('/app_details/', methods=['GET'])
def app_details():
    """ Returns project details.
        Output keys: ProjectName, Version, RootDirectory, HostName.
    """
    data = Config.get_project_details()
    return jsonify(ProjectName=data.metadata.PROJECT_NAME,
                   Version=data.metadata.VERSION,
                   RootDirectory=current_app.config.get('BASEDIR'),
                   HostName=current_app.config.get('COMPUTER_NAME'))


@details.route('/help/', methods=['GET'])
@details.route('/help/<method>/', methods=['GET'])
def help(method=None):
    """ Returns docs for given method or if not specified list of docs for all service methods.
        Input args: /method/.
        Output keys: api_methods: {<method_name>} or <method_name>.
    """

    def format_doc(function):
        if function.__doc__ is None:
            return ""
        doc = list(map(lambda x: x.lstrip(), function.__doc__.split('\n')))
        if doc[-1] == "":
            doc.pop()
        return " ".join(doc)

    methods = ServiceMethods.get()
    api_methods = {method.__name__: format_doc(method) for method in methods}
    if not method:
        return jsonify(api_methods=api_methods)
    try:
        documentation = api_methods[method]
    except KeyError:
        return jsonify(message='There is no method in api with that name.'), 404
    return jsonify({method: documentation})


@details.route('/info/')
def info():
    return render_template('details/details.html')


@details.route('/methods/')
def methods():
    return render_template('details/methods.html')
