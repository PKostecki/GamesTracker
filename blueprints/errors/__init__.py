from flask import Blueprint
from . import error_handler

bp = Blueprint('errors', __name__)


