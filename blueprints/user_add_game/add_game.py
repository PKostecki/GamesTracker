from flask import render_template, Blueprint, request, redirect, session
from log_required import login_required
from database import DatabaseExecutes
import os
import time

add_game_blueprint = Blueprint("add_game", __name__, template_folder='templates')
database_executor = DatabaseExecutes(os.path.join("gametracker_database.db"))


@add_game_blueprint.route('', methods=['POST', 'GET'])
@login_required
def user_add_game():
    if request.method == 'GET':
        games_from_database = database_executor.get_select_list("""SELECT game_name FROM games;""")
        print(games_from_database)
        return render_template('add_game.html', games=games_from_database)
    if request.method == 'POST':
        timestamp = time.time()
        game = request.form['game']
        comleption_date = request.form['completion']
        rate = request.form['rate']
        review = request.form['review']
        add_game_to_database(game)
        game_id = get_game_id(game)
        user_id = get_user_id()
        add_record(game_id, comleption_date, rate, review, user_id, timestamp)
        return redirect('dashboard')


def add_record(game_id, finish_date, record_grade, record_review, user_id, creation_timestamp):
    database_executor.execute_query(f"""INSERT INTO records ('game_id', 'game_finish_date', 'record_grade', 
    'record_review', 'user_id', 'creation_timestamp') VALUES ('{game_id}', '{finish_date}', '{record_grade}',
    '{record_review}', '{user_id}', '{creation_timestamp}');""")
    print('added record successfully')


def add_game_to_database(game):
    games_from_database = database_executor.get_select_list("""SELECT game_name FROM games;""")
    if game in games_from_database:
        pass
    else:
        timestamp = time.time()
        database_executor.execute_query(f"""INSERT INTO games ('game_name', 'creation_timestamp')
         VALUES ('{game}', '{timestamp}');""")
        print('added game to database')


def get_game_id(game):
    game_id = database_executor.select_single_element(f"""SELECT game_id FROM games WHERE game_name == '{game}';""")
    return game_id[0]


def get_user_id():
    user = session["name"]
    user_id = database_executor.select_single_element(f"""SELECT user_id FROM users WHERE user_nickname == '{user}';""")
    return user_id[0]
