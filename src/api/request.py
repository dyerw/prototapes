from flask.ext.restful import Resource, reqparse, abort

from api import abort_if_not_signed_in


class RequestApi(Resource):
    def post(self):
        abort_if_not_signed_in()

    def get(self):
        abort_if_not_signed_in()