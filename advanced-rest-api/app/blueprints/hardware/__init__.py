from flask import Blueprint

hardware = Blueprint('hardware',
                     __name__,
                     # url_prefix='/hardware',
                     template_folder='templates')

from app.blueprints.hardware import views
