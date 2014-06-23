import unittest
import json

from prototapes import app
from database import db


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

    def tearDown(self):
        with app.app_context():
            db.drop_all()

if __name__ == '__main__':
    unittest.main()