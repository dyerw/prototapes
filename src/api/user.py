from flask.ext.restful import Resource, reqparse, abort

from database import db, User


class UserApi(Resource):
    def user_exists(self, user):
        return len(User.query.filter_by(username=user).all()) > 0

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        args = parser.parse_args()

        # Validation checks on user input
        if self.user_exists(args['username']):
            abort(400, message='User already exists')

        if len(args['password']) < 6 or len(args['password']) > 150:
            abort(400, message='Password is an incorrect length')

        if len(args['username']) < 1 or len(args['username']) > 10:
            abort(400, message='Username is an incorrect length')

        new_user = User(args['username'], args['password'], args['email'])
        db.session.add(new_user)
        db.session.commit()

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        args = parser.parse_args()

        if not self.user_exists(args['username']):
            abort(404, message='User does not exist')