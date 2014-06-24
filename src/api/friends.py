from flask import session
from flask.ext.restful import Resource, abort

from api import abort_if_not_signed_in
from database import Friends


class FriendsApi(Resource):
    def get(self):
        abort_if_not_signed_in()

        friends = Friends.query.filter_by(friend1=session['username']).all()
        return friends