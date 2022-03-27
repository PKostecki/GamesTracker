from flask import render_template, Blueprint, request, redirect, url_for, session, flash
from log_required import login_required
from database import DatabaseExecutes
import os
import bcrypt

user_changes_blueprint = Blueprint("user_changes", __name__, template_folder='templates')
database_executor = DatabaseExecutes(os.path.join("gametracker_database.db"))


@user_changes_blueprint.route('/description/<username>', methods=['POST', 'GET'])
@login_required
def change_description(username):
    session_user = session["name"]
    if request.method == 'POST':
        if session_user == username:
            user_id = get_user_id(username)
            description = request.form.get('description')
            change_user_description(description, user_id)
            return redirect(url_for('dashboard.dashboard'))
        return redirect(url_for('user_profile.user', username=session_user))
    else:
        return render_template('user_change_description.html', username=username)


@user_changes_blueprint.route('/password/<username>', methods=['POST', 'GET'])
@login_required
def change_password(username):
    if request.method == 'POST':
        session_user = session["name"]
        if session_user == username:
            pin = request.form['password']
            if check_forms_length(pin):
                flash('Password must have at least 4 characters')
                return render_template('user_change_password.html', username=username)
            else:
                user_id = get_user_id(username)
                hashed_password = create_hash(pin)
                change_user_password(hashed_password, user_id)
                return redirect(url_for('dashboard.dashboard'))
        else:
            return redirect(url_for('user_profile.user', username=session_user))
    return render_template('user_change_password.html', username=username)


def get_user_id(username):
    user_id = database_executor.select_single_element(f"""SELECT user_id FROM
     users WHERE user_nickname == '{username}';""")
    return user_id[0]


def change_user_description(new_description, user_id):
    query = database_executor.execute_query(
        f"""UPDATE users SET description = '{new_description}' WHERE user_id = {user_id};""")
    return query


def create_hash(pin):
    salt = bcrypt.gensalt(14)
    hashed_salted_password = bcrypt.hashpw(pin.encode(), salt)
    return hashed_salted_password.decode()


def check_forms_length(checked_string):
    valid = len(checked_string)
    if valid < 4:
        return True


def change_user_password(new_password, user_id):
    query = database_executor.execute_query(
        f"""UPDATE users SET user_pin = '{new_password}' WHERE user_id = {user_id};""")
    return query
