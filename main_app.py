from flask import Flask
from flask_session import Session
from config import Config
from flask_basicauth import BasicAuth
from flask_mail import Mail
from flask_admin import Admin
from blueprints.login.login import login_blueprint
from blueprints.create_account.register import register_blueprint
from blueprints.dashboard.dashboard import dashboard_blueprint
from blueprints.user_games.user_games import user_games_blueprint
from blueprints.user_add_game.add_game import add_game_blueprint
from blueprints.users.users import users_blueprint
from blueprints.user_profile.user_profile import user_profile_blueprint
from blueprints.errors import errors_blueprint
from blueprints.email_handler.email_handler import email_handler_blueprint
from blueprints.user_changes.user_changes import user_changes_blueprint


app = Flask(__name__, template_folder='templates')
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config.from_object(Config)
app.app_context().push()
app.config['BASIC_AUTH_USERNAME'] = Config.auth_username
app.config['BASIC_AUTH_PASSWORD'] = Config.auth_password
basic_auth = BasicAuth(app)
Session(app)
mail = Mail(app)
app.register_blueprint(login_blueprint, url_prefix="/login")
app.register_blueprint(register_blueprint, url_prefix="/register")
app.register_blueprint(dashboard_blueprint, url_prefix="/dashboard")
app.register_blueprint(user_games_blueprint, url_prefix="/userlist")
app.register_blueprint(add_game_blueprint, url_prefix="/add")
app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(user_profile_blueprint, url_prefix="/user")
app.register_blueprint(errors_blueprint)
app.register_blueprint(email_handler_blueprint)
app.register_blueprint(user_changes_blueprint, url_prefix="/change")
from models import db_session, User, Games, MyModelView, UserView
admin = Admin(app)
admin.add_view(UserView(User, db_session))
admin.add_view(MyModelView(Games, db_session))


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
