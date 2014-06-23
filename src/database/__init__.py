from flask import session
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()
from request import Request
from user import User
from friends import Friends


def is_signed_in():
    return 'username' in session