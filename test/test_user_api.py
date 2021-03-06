import unittest
import json

from prototapes import app
from database import db


class TestUserPost(unittest.TestCase):
    def setUp(self):
        # Change the database to a test one in memory and
        # create all our tables there
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        with app.app_context():
            db.create_all()
        self.app = app.test_client()

    def test_incomplete_data(self):
        # Fails due to incomplete data
        response = self.app.post("/user")
        self.assertEqual(response.status_code, 400)

    def test_correct_data(self):
        # Passes because all data is provided
        response = self.app.post("/user", data=dict(username='test_user',
                                 password='abc123', email='asd@asd.com'))
        self.assertEqual(response.status_code, 200)

    def test_user_already_exists(self):
        # Create a user
        self.app.post("/user", data=dict(username='test_user',
                                 password='abc123', email='asd@asd.com'))

        # Fails because user already exists
        response = self.app.post("/user", data=dict(username='test_user',
                                 password='abc123', email='asd@asd.com'))
        message = json.loads(response.data)['message']
        self.assertEqual(response.status_code, 400)
        self.assertEqual(message, 'User already exists')

    def test_password_too_short(self):
        # Fails because password is too short
        response = self.app.post("/user", data=dict(username='test_user1',
                                 password='aa', email='asd@asd.com'))
        message = json.loads(response.data)['message']
        self.assertEqual(response.status_code, 400)
        self.assertEqual(message, 'Password is an incorrect length')

    def test_username_too_long(self):
        # Fails because username is too long
        response = self.app.post("/user", data=dict(username='1234567891011',
                                 password='abc123', email='asd@asd.com'))
        message = json.loads(response.data)['message']
        self.assertEqual(response.status_code, 400)
        self.assertEqual(message, 'Username is an incorrect length')

    def tearDown(self):
        with app.app_context():
            db.drop_all()


class TestUserGet(unittest.TestCase):
    """
    Test functionality to do with logging in.
    """
    def setUp(self):
        # Change the database to a test one in memory and
        # create all our tables there
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        with app.app_context():
            db.create_all()
        self.app = app.test_client()

    def test_user_does_not_exist(self):
        # Fails because user does not exist
        response = self.app.get("/user?username=test_user&password=abc123")
        self.assertEqual(response.status_code, 404)
        message = json.loads(response.data)['message']
        self.assertEqual(message, 'User does not exist')

    def test_username_not_given(self):
        # Fails because username is not provided
        response = self.app.get("/user?password=abc123")
        self.assertEqual(response.status_code, 400)

    def test_password_not_given(self):
        # Fails because username is not provided
        response = self.app.get("/user?username=test_user")
        self.assertEqual(response.status_code, 400)

    def test_invalid_password(self):
        # Add a user
        self.app.post("/user", data=dict(username='test_user',
                      password='abc123', email='asd@asd.com'))

        response = self.app.get('/user?username=test_user&password=wowowww')
        self.assertEqual(response.status_code, 401)
        message = json.loads(response.data)['message']
        self.assertEqual(message, 'Invalid password')

    def test_successful_login(self):
        # Add a user
        self.app.post("/user", data=dict(username='test_user',
                      password='abc123', email='asd@asd.com'))

        response = self.app.get('/user?username=test_user&password=abc123')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        with app.app_context():
            db.drop_all()