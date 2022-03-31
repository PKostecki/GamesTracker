from flask import redirect, url_for, request, render_template, flash, Blueprint, session
from database import DatabaseExecutes
import os
import bcrypt

login_blueprint = Blueprint("login", __name__, template_folder='templates')
database_executor = DatabaseExecutes(os.path.join("gametracker_database.db"))


@login_blueprint.route('', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['name']
        pin = request.form['pin']
        if check_pin(user, pin):
            session["name"] = user
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash('Wrong password')
            return render_template('login.html')
    else:
        return render_template('login.html')


def check_pin(nickname, pin):
    user_pin_hash = database_executor.select_single_element(
        f"""SELECT user_pin FROM users WHERE user_nickname = '{nickname}';""")
    # user_pin = select_single_element("""SELECT user_pin FROM users WHERE user_nickname = :nickname;""")
    if user_pin_hash is None:
        return False
    else:
        password_bytes = pin.encode()
        hash_bytes = user_pin_hash[0].encode()
        does_match = bcrypt.checkpw(password_bytes, hash_bytes)
        return does_match
