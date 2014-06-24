import unittest
import json

from prototapes import app
from database import db, Request


class TestRequestPost(unittest.TestCase):
    """
    Tests the API functionality to do with making friend requests
    """
    def setUp(self):
        # Change the database to a test one in memory and
        # create all our tables there
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        with app.app_context():
            db.create_all()
        self.app = app.test_client()

    def test_not_logged_in(self):
        """
        A request that does not come from a logged in user cannot
        make a friend request
        """
        response = self.app.get("/request?username=test_user2")
        self.assertEqual(response.status_code, 401)
        message = json.loads(response.data)['message']
        self.assertEqual(message, 'Not signed in')