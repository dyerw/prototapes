import hashlib

from flask import session
from flask.ext.restful import Resource, reqparse, abort

from database import db, User
from api import user_exists


class UserApi(Resource):
    def valid_password(self, username, password):
        user = User.query.filter_by(username=username).first()
        return user.password == hashlib.sha1(password + user.salt).hexdigest()

    def post(self):
        """
        Registers a new user if valid username, password, and email
        are given.
        """
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        args = parser.parse_args()

        # Validation checks on user input
        if user_exists(args['username']):
            abort(400, message='User already exists')

        if len(args['password']) < 6 or len(args['password']) > 150:
            abort(400, message='Password is an incorrect length')

        if len(args['username']) < 1 or len(args['username']) > 10:
            abort(400, message='Username is an incorrect length')

        new_user = User(args['username'], args['password'], args['email'])
        db.session.add(new_user)
        db.session.commit()

    def get(self):
        """
        Logs a user in if username and password supplied are valid.
        """
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()

        if not user_exists(args['username']):
            abort(404, message='User does not exist')

        if not self.valid_password(args['username'], args['password']):
            abort(401, message='Invalid password')

        session['username'] = args['username']