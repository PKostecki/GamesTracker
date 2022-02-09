from flask import render_template, Blueprint
from log_required import login_required

dashboard_blueprint = Blueprint("dashboard", __name__, template_folder='templates')


@dashboard_blueprint.route('', methods=['POST', 'GET'])
@login_required
def dashboard():
    return render_template('dashboard.html'), 201
