from flask import Blueprint

logs = Blueprint('logs',
                 __name__,
                 # url_prefix='/logs',
                 template_folder='templates')

from app.blueprints.logs import views
