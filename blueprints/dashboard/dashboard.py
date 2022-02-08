from flask import render_template, Blueprint

dashboard_blueprint = Blueprint("dashboard", __name__, template_folder='templates')


@dashboard_blueprint.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    return render_template('dashboard.html'), 201