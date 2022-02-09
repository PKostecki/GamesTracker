from flask import Flask
from flask_session import Session
import config
from blueprints.login.login import login_blueprint
from blueprints.create_account.register import register_blueprint
from blueprints.dashboard.dashboard import dashboard_blueprint


app = Flask(__name__, template_folder='templates')
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.register_blueprint(login_blueprint, url_prefix="/login")
app.register_blueprint(register_blueprint, url_prefix="/register")
app.register_blueprint(dashboard_blueprint, url_prefix="/dashboard")
app.secret_key = config.salted_secret_key


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
