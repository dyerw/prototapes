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
        response = self.app.post("/request", data={'username': 'something'})
        self.assertEqual(response.status_code, 401)
        message = json.loads(response.data)['message']
        self.assertEqual(message, 'Not signed in')

    def test_fails_because_no_username_provided(self):
        """
        A friend request requires a username be given
        """
        # Create and sign in the test user
        self.app.post("/user", data=dict(username='test_user',
                      password='abc123', email='asd@asd.com'))
        self.app.get("/user?username=test_user&password=abc123")

        response = self.app.post("/request")
        self.assertEqual(response.status_code, 400)

    def test_fails_because_user_does_not_exist(self):
        """
        User cannot make a request to another that does not exist
        """
        # Create and sign in the test user
        self.app.post("/user", data=dict(username='test_user',
                      password='abc123', email='asd@asd.com'))
        self.app.get("/user?username=test_user&password=abc123")

        response = self.app.post("/request", data={'username': 'something'})
        self.assertEqual(response.status_code, 404)
        message = json.loads(response.data)['message']
        self.assertEqual(message, 'User does not exist')

    def test_successful_new_request(self):
        """
        Friend request works between two users who are not friends
        """
        #Create two users
        self.app.post("/user", data=dict(username='test_user',
                      password='abc123', email='asd@asd.com'))
        self.app.post("/user", data=dict(username='test_user2',
                      password='abc456', email='asd2@asd.com'))

        # Sign user in
        self.app.get("/user?username=test_user&password=abc123")

        response = self.app.post("/request", data={'username': 'test_user2'})
        self.assertEqual(response.status_code, 200)
        message = json.loads(response.data)['message']
        self.assertEqual(message, 'Request sent')

    def test_fails_if_already_requested(self):
        """
        A user cannot send a friend request to a friend who has already
        been requested.
        """
        #Create two users
        self.app.post("/user", data=dict(username='test_user',
                      password='abc123', email='asd@asd.com'))
        self.app.post("/user", data=dict(username='test_user2',
                      password='abc456', email='asd2@asd.com'))

        # Sign user in
        self.app.get("/user?username=test_user&password=abc123")

        # Send one friend request
        self.app.post("/request", data={'username': 'test_user2'})

        response = self.app.post("/request", data={'username': 'test_user2'})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, 'Friend request already sent')

    def test_successful_new_friends(self):
        """
        If a user posts a request back to someone who has already requested them
        they become friends.
        """
        #Create two users
        self.app.post("/user", data=dict(username='test_user',
                      password='abc123', email='asd@asd.com'))
        self.app.post("/user", data=dict(username='test_user2',
                      password='abc456', email='asd2@asd.com'))

        # Sign user in
        self.app.get("/user?username=test_user&password=abc123")

        # Send one friend request
        self.app.post("/request", data={'username': 'test_user2'})

        # Log out current user
        self.app.get("/logout")

        # Sign in the other user
        self.app.get("/user?username=test_user2&password=abc456")

        # Send a second request
        response = self.app.post("/request", data={'username': 'test_user',
                                                   'approval': 'approve'})
        self.assertEqual(response.status_code, 200)
        message = json.loads(response.data)['message']
        self.assertEqual(message, 'Request approved')

    def test_fails_because_already_friends(self):
        """
        You cannot request someone who is already your friend
        """
        #Create two users
        self.app.post("/user", data=dict(username='test_user',
                      password='abc123', email='asd@asd.com'))
        self.app.post("/user", data=dict(username='test_user2',
                      password='abc456', email='asd2@asd.com'))

        # Sign user in
        self.app.get("/user?username=test_user&password=abc123")

        # Send one friend request
        self.app.post("/request", data={'username': 'test_user2'})

        # Log out current user
        self.app.get("/logout")

        # Sign in the other user
        self.app.get("/user?username=test_user2&password=abc456")

        # Send a second request, making them friends
        self.app.post("/request", data={'username': 'test_user',
                                        'approval': 'approve'})

        response = self.app.post("/request", data={'username': 'test_user'})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, 'Already friends')

    def test_success_because_request_dismissed(self):
        #Create two users
        self.app.post("/user", data=dict(username='test_user',
                      password='abc123', email='asd@asd.com'))
        self.app.post("/user", data=dict(username='test_user2',
                      password='abc456', email='asd2@asd.com'))

        # Sign user in
        self.app.get("/user?username=test_user&password=abc123")

        # Send one friend request
        self.app.post("/request", data={'username': 'test_user2'})

        # Log out current user
        self.app.get("/logout")

        # Sign in the other user
        self.app.get("/user?username=test_user2&password=abc456")

        # Send a second request
        response = self.app.post("/request", data={'username': 'test_user',
                                                   'approval': 'dismiss'})
        self.assertEqual(response.status_code, 200)
        message = json.loads(response.data)['message']
        self.assertEqual(message, 'Request dismissed')

        # Test that we can now send another friend request
        # this verifies that the last request was removed
        response = self.app.post("/request", data={'username': 'test_user'})
        self.assertEqual(response.status_code, 200)
        message = json.loads(response.data)['message']
        self.assertEqual(message, 'Request sent')

    def tearDown(self):
        with app.app_context():
            db.drop_all()