from flask import session
from flask.ext.restful import abort


def abort_if_not_signed_in():
    if 'username' not in session:
        abort(401, message="Not signed in")