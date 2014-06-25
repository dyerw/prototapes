from flask import session
from flask.ext.restful import Resource, reqparse, abort

from api import abort_if_not_signed_in, user_exists, are_friends
from database.request import Request
from database.friends import Friends
from database import db


class RequestApi(Resource):
    def request_sent(self, requester, requestee):
        results = Request.query.filter_by(requester=requester, requestee=requestee).all()
        return len(results) > 0

    def post(self):
        abort_if_not_signed_in()
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('approval', type=str)
        args = parser.parse_args()

        # Set default of approve for approval
        if not 'approval' in args:
            args['approval'] = 'approve'

        if not user_exists(args['username']):
            abort(404, message="User does not exist")

        if are_friends(args['username'], session['username']):
            abort(400, message="Already friends")

        if self.request_sent(session['username'], args['username']):
            abort(400, message="Friend request already sent")

        # If request has already been sent by the person this request is
        # requesting, they become friends or dismiss the request
        if self.request_sent(args['username'], session['username']):
            # We either dismiss the request or become friends
            if args['approval'] == 'approve':
                new_friends = Friends(session['username'], args['username'])
                db.session.add(new_friends)
                db.session.commit()
                return {'message': 'Request approved'}
            else:
                request = Request.query.filter_by(requester=args['username'], requestee=session['username']).first()
                db.session.delete(request)
                db.session.commit()
                return {'message': 'Request dismissed'}

        new_request = Request(session['username'], args['username'])
        db.session.add(new_request)
        db.session.commit()

        return {'message': 'Request sent'}

    def get(self):
        abort_if_not_signed_in()