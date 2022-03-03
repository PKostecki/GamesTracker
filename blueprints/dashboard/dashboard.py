from flask import render_template, Blueprint, request, redirect, url_for, session
from log_required import login_required
from flask_login import logout_user

dashboard_blueprint = Blueprint("dashboard", __name__, template_folder='templates')


@dashboard_blueprint.route('', methods=['POST', 'GET'])
@login_required
def dashboard():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Home':
            return redirect(url_for('dashboard.dashboard'))
        if request.form['submit_button'] == 'Add game':
            return redirect(url_for('add_game.user_add_game'))
        if request.form['submit_button'] == 'My games':
            return redirect(url_for('user_games_list.user_games_list'))
        if request.form['submit_button'] == 'Users':
            return redirect(url_for('users.users'))
        if request.form['submit_button'] == 'Logout':
            session.pop('name', None)
            return redirect(url_for('login.login'))
    else:
        return render_template('dashboard.html'), 201





