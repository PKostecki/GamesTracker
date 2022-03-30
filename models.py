from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, Column, VARCHAR, INTEGER
from sqlalchemy.orm import Session
from main_app import basic_auth
from werkzeug.exceptions import HTTPException
from flask import Response, redirect
from flask_admin.contrib.sqla import ModelView
import time

# automap base
Base = automap_base()


class User(Base):
    __tablename__ = 'users'
    user_id = Column('user_id', INTEGER, primary_key=True)
    user_nickname = Column('user_nickname', VARCHAR(40), unique=True)
    user_pin = Column('user_pin', VARCHAR(200))
    description = Column('description', VARCHAR(100))
    creation_timestamp = Column('creation_timestamp', INTEGER, default=time.time())
    user_email = Column('user_email', VARCHAR(100), unique=True)


class Games(Base):
    __tablename__ = 'games'
    game_id = Column('game_id', INTEGER, primary_key=True)
    game_name = Column('game_name', VARCHAR(100), unique=True)
    creation_timestamp = Column('creation_timestamp', INTEGER, default=time.time())


class AuthException(HTTPException):
    def __init__(self, message):
        super().__init__(message, Response(
            "You could not be authenticated. Please refresh the page.", 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}))


class MyModelView(ModelView):
    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException('Not authenticated.')
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())


class UserView(MyModelView):
    column_exclude_list = ['user_pin']
    column_searchable_list = ['user_nickname']


engine = create_engine("sqlite:///gametracker_database.db", connect_args={'check_same_thread': False})
Base.prepare(engine, reflect=True)
db_session = Session(engine)
