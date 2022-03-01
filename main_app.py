from flask import Flask
from flask_session import Session
import config
from blueprints.login.login import login_blueprint
from blueprints.create_account.register import register_blueprint
from blueprints.dashboard.dashboard import dashboard_blueprint
from blueprints.user_games.user_games import user_games_blueprint
from blueprints.user_add_game.add_game import add_game_blueprint
from blueprints.users.users import users_blueprint
from blueprints.user_profile.user_profile import user_profile_blueprint


app = Flask(__name__, template_folder='templates')
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.register_blueprint(login_blueprint, url_prefix="/login")
app.register_blueprint(register_blueprint, url_prefix="/register")
app.register_blueprint(dashboard_blueprint, url_prefix="/dashboard")
app.register_blueprint(user_games_blueprint, url_prefix="/userlist")
app.register_blueprint(add_game_blueprint, url_prefix="/add")
app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(user_profile_blueprint, url_prefix="/user")
app.secret_key = config.salted_secret_key


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
