from flask import Blueprint

params = Blueprint('params',
                   __name__,
                   # url_prefix='/params',
                   template_folder='templates')

from app.blueprints.params import views
