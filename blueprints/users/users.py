from flask import render_template, Blueprint, request, redirect
from log_required import login_required
from database import DatabaseExecutes
import os

users_blueprint = Blueprint("users", __name__, template_folder='templates')
database_executor = DatabaseExecutes(os.path.join("gametracker_database.db"))


@users_blueprint.route('', methods=['POST', 'GET'])
@login_required
def users():
    if request.method == 'POST':
        return redirect('user_profile')
    else:
        users_list = get_users_list()
        return render_template('users.html', users=users_list)


def get_users_list():
    users_list = database_executor.get_select_list(f"""SELECT user_nickname FROM users;""")
    return users_list
