from flask import session
from flask.ext.restful import abort

from database.user import User
from database.friends import Friends


def abort_if_not_signed_in():
    if 'username' not in session:
        abort(401, message="Not signed in")


def user_exists(user):
    return len(User.query.filter_by(username=user).all()) > 0


def are_friends(user1, user2):
    sel1 = Friends.query.filter_by(friend1=user1, friend2=user2).all()
    sel2 = Friends.query.filter_by(friend1=user2, friend2=user1).all()
    return len(sel1) > 0 or len(sel2) > 0