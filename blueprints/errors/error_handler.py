from blueprints.errors import bp
from flask import render_template


@bp.app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@bp.app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500
