from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()
from request import Request
from user import User
from friends import Friends