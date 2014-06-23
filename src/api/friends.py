from flask import session
from flask.ext.restful import Resource, abort

from database import db, Friends, is_signed_in


class FriendsApi(Resource):
    def get(self):
        if not is_signed_in():
            abort(500, message="Not signed in")

        friends = Friends.query.filter_by(friend1=session['username']).all()
        return friends