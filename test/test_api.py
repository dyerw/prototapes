import unittest
import json

from flask import session

from prototapes import app
from database import db, Request


class ApiTests(unittest.TestCase):
    def setUp(self):
        # Change the database to a test one in memory and
        # create all our tables there
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        with app.app_context():
            db.create_all()
        self.app = app.test_client()

    def test_server_is_up(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)

    def test_user_post(self):
        # Fails due to incomplete data
        response = self.app.post("/user")
        self.assertEqual(response.status_code, 400)

        # Passes because all data is provided
        response = self.app.post("/user", data=dict(username='test_user',
                                 password='abc123', email='asd@asd.com'))
        self.assertEqual(response.status_code, 200)

        # Fails because user already exists
        response = self.app.post("/user", data=dict(username='test_user',
                                 password='abc123', email='asd@asd.com'))
        message = json.loads(response.data)['message']
        self.assertEqual(response.status_code, 400)
        self.assertEqual(message, 'User already exists')

        # Fails because password is too short
        response = self.app.post("/user", data=dict(username='test_user1',
                                 password='aa', email='asd@asd.com'))
        message = json.loads(response.data)['message']
        self.assertEqual(response.status_code, 400)
        self.assertEqual(message, 'Password is an incorrect length')

        # Fails because username is too long
        response = self.app.post("/user", data=dict(username='1234567891011',
                                 password='abc123', email='asd@asd.com'))
        message = json.loads(response.data)['message']
        self.assertEqual(response.status_code, 400)
        self.assertEqual(message, 'Username is an incorrect length')

    def test_user_get(self):
        # Fails because username is not provided
        response = self.app.get("/user")
        self.assertEqual(response.status_code, 400)

        # Fails because user does not exist
        response = self.app.get("/user?username=test_user")
        self.assertEqual(response.status_code, 404)
        message = json.loads(response.data)['message']
        self.assertEqual(message, 'User does not exist')

        # Add a user
        self.app.post("/user", data=dict(username='test_user',
                      password='abc123', email='asd@asd.com'))

        # Succeeds because user exists
        response = self.app.get('/user?username=test_user')
        self.assertEqual(response.status_code, 200)

    def test_request_post(self):
        # Fails because user is not logged in
        # so no session is available
        response = self.app.get("/request?username=test_user2")
        self.assertEqual(response.status_code, 401)
        message = json.loads(response.data)['message']
        self.assertEqual(message, 'Not signed in')

        # "Log in" the user
        with self.app.test_request_context():
            session['username'] = 'test_user'

        print self.app.get('/session').data

        # Succeeds and adds a request to the database
        response = self.app.get("/request?username=test_user2")
        self.assertEqual(response.status_code, 200)
        result = Request.query.filter_by(requester='test_user').first()
        self.assertEqual(result, 'test_user2')

        # Fails because a request has already been made

    def tearDown(self):
        with app.app_context():
            db.drop_all()

if __name__ == '__main__':
    unittest.main()