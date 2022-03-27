from flask import redirect, url_for, request, render_template, flash, Blueprint
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
        email = request.form['email']
        pin = request.form['pin']
        string_hash = create_hash(pin)
        description = request.form['description']
        if check_forms_length(user) and check_forms_length(pin):
            flash('Nickname and password must have at least 4 characters')
            return render_template('register.html')
        if check_user_exist(user):
            flash('Nickname already used')
            return render_template('register.html')
        else:
            add_user_to_database(user, string_hash, description, email)
            return redirect(url_for('login.login'))
    else:
        return render_template('register.html')


def check_forms_length(checked_string):
    valid = len(checked_string)
    if valid < 4:
        return True


def add_user_to_database(nickname, pin, user_description, user_email):
    timestamp = time.time()
    database_executor.execute_query(f"INSERT INTO users(user_nickname, user_pin, description, "
                                    f"creation_timestamp, user_email) VALUES ('{nickname}',"
                                    f"'{pin}', '{user_description}', '{timestamp}', '{user_email}');")
