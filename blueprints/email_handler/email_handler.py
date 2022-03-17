from flask import redirect, url_for, request, render_template, flash, Blueprint, session
from database import DatabaseExecutes
import os
import jwt
from flask_mail import Message
from time import time
import bcrypt
import threading


email_handler_blueprint = Blueprint("reset", __name__, template_folder='templates')
database_executor = DatabaseExecutes(os.path.join("gametracker_database.db"))
from main_app import mail
from config import Config


@email_handler_blueprint.route('/reset', methods=['POST', 'GET'])
def send_pass_reset():
    if request.method == 'POST':
        user = session.get("name")
        if user is None:
            email = request.form['email']
            if check_email_exist(email):
                token = get_reset_pass_token(email)
                flash("Email with reset instruction sent")
                thread = threading.Thread(target=send_email('Password reset', sender=Config.MAIL_USERNAME,
                                                            recipients=[email],
                                                            text_body=render_template('reset_password_message.txt',
                                                                                      email=email, token=token),
                                                            html_body=render_template('reset_password_message.html',
                                                                                      email=email, token=token)))
                thread.daemon = True
                thread.start()
                return redirect(url_for('login.login'))
            else:
                flash('Email doesnt exist')
                return render_template('reset_password_request.html')
        else:
            return redirect(url_for('dashboard.dashboard'))
    else:
        return render_template('reset_password_request.html')


@email_handler_blueprint.route('/reset_password/<token>', methods=['POST', 'GET'])
def reset_password(token):
    user_id = verify_reset_password_token(token)
    user = session.get("name")
    if user:
        return redirect(url_for('dashboard.dashboard'))
    if not user_id:
        return redirect(url_for('login.login'))
    if request.method == 'POST':
        pin = request.form['password']
        if check_forms_length(pin):
            flash('Password must have at least 4 characters')
            return render_template('reset_password.html', token=token)
        else:
            hashed_password = create_hash(pin)
            change_user_password(hashed_password, user_id)
            return redirect(url_for('login.login'))
    return render_template('reset_password.html', token=token)


def get_reset_pass_token(user_email, expires_in=600):
    return jwt.encode({'reset_password': user_email, 'exp': time() + expires_in},
                      Config.secret_key, algorithm='HS256')


def verify_reset_password_token(token):
    try:
        user_email = jwt.decode(token, Config.secret_key,
                                algorithms=['HS256'])['reset_password']
    except:
        return
    return get_user_id(user_email)


def get_user_id(user_email):
    user_id = database_executor.select_single_element(f"""SELECT user_id FROM
     users WHERE user_email == '{user_email}';""")
    return user_id[0]


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


def check_email_exist(email):
    email_database = database_executor.select_single_element(
        f"""SELECT user_email FROM users WHERE user_email = '{email}';""")
    try:
        if email_database[0] == email:
            return True
    except:
        pass


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
