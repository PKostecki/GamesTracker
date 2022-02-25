from flask import Flask, redirect, url_for, request, render_template, flash, Blueprint
from database import DatabaseExecutes
import os
import bcrypt
import time

register_blueprint = Blueprint("register", __name__, template_folder='templates')
database_executor = DatabaseExecutes(os.path.join("gametracker_database.db"))


def check_user_exist(nickname):
    user_database = database_executor.select_single_element(
        f"""SELECT user_nickname FROM users WHERE user_nickname = '{nickname}';""")
    try:
        if user_database[0] == nickname:
            return True
    except:
        print(f"User added to database")
        pass


def create_hash(pin):
    salt = bcrypt.gensalt(14)
    hashed_salted_password = bcrypt.hashpw(pin.encode(), salt)
    return hashed_salted_password.decode()


@register_blueprint.route('', methods=['POST', 'GET'])
def create_account():
    if request.method == 'POST':
        user = request.form['name']
        pin = request.form['pin']
        string_hash = create_hash(pin)
        description = request.form['description']
        if check_user_exist(user):
            flash('Nickname already used')
            return render_template('register.html')
        else:
            add_user_to_database(user, string_hash, description)
            return redirect(url_for('login.login'))
    else:
        user = request.args.get('name')
        return render_template('register.html')


def add_user_to_database(nickname, pin, user_description):
    timestamp = time.time()
    database_executor.execute_query(f"INSERT INTO users(user_nickname, user_pin, description, "
                                    f"creation_timestamp) VALUES ('{nickname}',"
                                    f"'{pin}', '{user_description}', '{timestamp}');")