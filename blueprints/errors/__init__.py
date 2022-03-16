from flask import Blueprint

errors_blueprint = Blueprint('errors', __name__, template_folder='templates')

from blueprints.errors import error_handler
