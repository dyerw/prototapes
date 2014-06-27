from flask import session
from flask.ext.restful import Resource

from api import abort_if_not_signed_in
from database import Friends


class FriendsApi(Resource):
    def get(self):
        abort_if_not_signed_in()

        friends = Friends.query.filter_by(friend1=session['username']).all()
        friends2 = Friends.query.filter_by(friend2=session['username']).all()
        friends = [f.friend2 for f in friends]
        friends2 = [f.friend1 for f in friends2]
        return friends + friends2