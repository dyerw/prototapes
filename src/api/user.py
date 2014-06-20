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

        if self.user_exists(args['username']):
            abort(400, message='User already exists')

        new_user = User(args['username'], args['password'], args['email'])
        db.session.add(new_user)
        db.session.commit()

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        args = parser.parse_args()

        if not self.user_exists(args['username']):
            abort(404, message='User does not exist')