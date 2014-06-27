import unittest
import json
import os
from StringIO import StringIO

from werkzeug.datastructures import FileStorage

from prototapes import app
from database import db
from database.song import Song

HERE = os.path.abspath(os.path.dirname(__file__))


class TestSongPost(unittest.TestCase):
    def setUp(self):
        # Change the database to a test one in memory and
        # create all our tables there
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['UPLOAD_LOCATION'] = os.path.join(HERE, 'test_uploads')
        with app.app_context():
            db.create_all()
        self.app = app.test_client()

        # Create a test user
        self.app.post("/user", data={'username': 'test_user',
                                     'password': 'password',
                                     'email': 'asd@asd.com'})

        with open(os.path.join('test_data', 'test.mp3'), 'rb') as f:
            self.mp3_file = f.read()

        with open(os.path.join('test_data', 'test.txt'), 'rb') as f:
            self.text_file = f.read()

    def test_failure_because_not_signed_in(self):
        response = self.app.post("/song")
        self.assertEqual(response.status_code, 401)

    def test_no_filetype_provided(self):
        self.app.get("/user?username=test_user&password=password")
        response = self.app.post("/song", data={'artist': 'an artist',
                                                'title': 'a title',
                                                'album': 'a album',
                                                'file': self.mp3_file})
        self.assertEqual(response.status_code, 400)

    def test_no_artist_provided(self):
        self.app.get("/user?username=test_user&password=password")
        response = self.app.post("/song",
                                 content_type='multipart/form-data',
                                 data={'filetype': 'mp3 (320)',
                                        'title': 'a title',
                                        'album': 'a album',
                                        'file': self.mp3_file})
        self.assertEqual(response.status_code, 400)

    def test_no_title_provided(self):
        self.app.get("/user?username=test_user&password=password")
        response = self.app.post("/song", data={'artist': 'an artist',
                                                'filetype': 'mp3 (320)',
                                                'album': 'a album',
                                                'file': self.mp3_file})
        self.assertEqual(response.status_code, 400)
        
    def test_no_album_provided(self):
        self.app.get("/user?username=test_user&password=password")
        response = self.app.post("/song", data={'artist': 'an artist',
                                                'title': 'a title',
                                                'filetype': 'mp3 (320)',
                                                'file': self.mp3_file})
        self.assertEqual(response.status_code, 400)

    def test_no_file_provided(self):
        self.app.get("/user?username=test_user&password=password")
        response = self.app.post("/song", data={'artist': 'an artist',
                                                'title': 'a title',
                                                'filetype': 'mp3 (320)',
                                                'album': 'a album'})
        self.assertEqual(response.status_code, 400)

    def test_not_allowed_file_extension(self):
        self.app.get("/user?username=test_user&password=password")
        response = self.app.post("/song",
                                 content_type='multipart/form-data',
                                 data={'artist': 'an artist',
                                       'title': 'a title',
                                       'filetype': 'mp3 (320)',
                                       'album': 'a album',
                                       'file': (StringIO(self.mp3_file),
                                                'test.txt')})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "File extension not allowed")

    def test_not_allowed_file_type(self):
        self.app.get("/user?username=test_user&password=password")
        response = self.app.post("/song",
                                 content_type='multipart/form-data',
                                 data={'artist': 'an artist',
                                       'title': 'a title',
                                       'filetype': 'mp3 (320)',
                                       'album': 'a album',
                                       'file': (StringIO(self.text_file),
                                                'test.mp3')})
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "File type not allowed")

    def test_successful_file_upload(self):
        # Clear the upload folder
        for file in os.listdir(app.config['UPLOAD_LOCATION']):
            file_path = os.path.join(app.config['UPLOAD_LOCATION'], file)
            os.unlink(file_path)

        self.app.get("/user?username=test_user&password=password")
        response = self.app.post("/song",
                                 content_type='multipart/form-data',
                                 data={'artist': 'an artist',
                                       'title': 'a title',
                                       'filetype': 'mp3 (320)',
                                       'album': 'a album',
                                       'file': (StringIO(self.mp3_file),
                                                'test.mp3')})
        self.assertEqual(response.status_code, 200)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "Song uploaded")

        # Check that there is a file in the upload location
        self.assertEqual(1, len(os.listdir(app.config['UPLOAD_LOCATION'])))
