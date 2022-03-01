from flask import render_template, Blueprint, request
from log_required import login_required
from database import DatabaseExecutes
import os

user_profile_blueprint = Blueprint("user_profile", __name__, template_folder='templates')
database_executor = DatabaseExecutes(os.path.join("gametracker_database.db"))


@user_profile_blueprint.route('/<username>', methods=['POST', 'GET'])
@login_required
def user(username):
    if request.method == 'POST':
        return render_template('user_profile.html')
    else:
        description = get_user_description(username)
        records_info = get_record_info(username)
        new_games_list = []
        for record_info in records_info:
            game_id = record_info[0]
            game_name = get_game_name(game_id)
            new_game_tuple = (game_name, *record_info[1:])
            new_games_list.append(new_game_tuple)
        print(new_games_list)
        print(description)
        return render_template('user_profile.html', user=username, description=description,
                               record_info=new_games_list)


def get_game_name(game_id):
    game_name = database_executor.select_single_element(f"""SELECT game_name FROM games WHERE
     game_id == '{game_id}';""")
    if game_name is not None:
        game_name = game_name[0]
    return game_name


def get_user_id(username):
    user_id = database_executor.select_single_element(f"""SELECT user_id FROM users WHERE
     user_nickname == '{username}';""")
    return user_id[0]


def get_record_info(username):
    user_id = get_user_id(username)
    record_info = database_executor.get_records_query(f"""SELECT game_id, game_finish_date, record_grade,
     record_review
     FROM records WHERE user_id == '{user_id}';""")
    return record_info


def get_user_description(username):
    description = database_executor.get_select_list(f"""SELECT description FROM users
     WHERE user_nickname = '{username}';""")
    return description[0]
