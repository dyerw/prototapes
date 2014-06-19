import uuid
import hashlib

from database import db


class User(db.Model):
    username = db.Column(db.String(10), primary_key=True)
    password = db.Column(db.String(150))
    salt     = db.Column(db.String(100))
    email    = db.Column(db.String(30), unique=True)

    def __init__(self, username, password, email):
        self.username = username
        self.email    = email
        self.salt     = str(uuid.uuid4()).replace("-", "")
        self.password = hashlib.sha1(password + self.salt).hexdigest()

    def __repr__(self):
        return "<User %r>" % self.username