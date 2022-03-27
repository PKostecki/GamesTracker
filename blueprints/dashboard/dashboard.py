from flask import render_template, Blueprint, request, redirect, url_for, session
from log_required import login_required
from database import DatabaseExecutes
import os

dashboard_blueprint = Blueprint("dashboard", __name__, template_folder='templates')
database_executor = DatabaseExecutes(os.path.join("gametracker_database.db"))


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
        if request.form['submit_button'] == 'Profile':
            user = session["name"]
            return redirect(url_for('user_profile.user', username=user))
    else:
        record_info = get_records()
        last_records_list = []
        for game, grade, user_id in record_info:
            game_name = get_game_name(game)
            user = get_user(user_id)
            last_record_tuple = (game_name, grade, *user)
            last_records_list.append(last_record_tuple)
        return render_template('dashboard.html', last_records_list=last_records_list[-5:]), 201


def get_records():
    record_info = database_executor.get_records_query("""SELECT game_id, record_grade,  user_id FROM  
    records;""")
    return record_info


def get_game_name(game_id):
    game_name = database_executor.select_single_element(f"""SELECT game_name FROM games WHERE
     game_id == '{game_id}';""")
    if game_name is not None:
        game_name = game_name[0]
    return game_name


def get_user(user_id):
    user = database_executor.get_select_list(f"""SELECT user_nickname FROM users WHERE user_id = '{user_id}';""")
    return user
