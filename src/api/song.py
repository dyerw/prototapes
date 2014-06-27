import os

from flask import request, abort
from werkzeug.utils import secure_filename
from flask.ext.restful import Resource, reqparse

from database import db, Song
from api import abort_if_not_signed_in

ALLOWED_EXTENSIONS = {'mp3', 'flac', 'wav'}


class SongApi(Resource):

    def allowed_extension(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

    def post(self):
        """
        Registers a new user if valid username, password, and email
        are given.
        """
        abort_if_not_signed_in()
        parser = reqparse.RequestParser()
        parser.add_argument('filetype', type=str, required=True)
        parser.add_argument('artist', type=str, required=True)
        parser.add_argument('title', type=str, required=True)
        parser.add_argument('album', type=str, required=True)
        args = parser.parse_args()

        upload_file = request.files['file']

        # Make sure the file has an allowed extension
        if not self.allowed_extension(upload_file.filename):
            abort(400, message="File extension not allowed")

        # Allow werkzeug to do its security magic
        filename = secure_filename(request.files['file'].filename)

        # Add a new song to the database
        new_song = Song(filename, args['filetype'], args['title'],
                        args['artist'], args['album'])
        db.session.add(new_song)
        db.session.commit()

        # Save the file to the appropriate location
        from prototapes import app
        if 's3' in app.config['UPLOAD_LOCATION']:
            # do s3 stuff
            pass
        else:
            # We want to upload to a local directory
            upload_file.save(os.path.join(app.config['UPLOAD_LOCATION'],
                                          new_song.song_id))


        return {'message': 'Song uploaded'}