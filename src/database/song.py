import uuid
import datetime

from database import db


class Song(db.Model):
    song_id     = db.Column(db.String(30), primary_key=True)
    filename    = db.Column(db.String(100))
    filetype    = db.Column(db.String(10))
    title       = db.Column(db.String(100))
    artist      = db.Column(db.String(100))
    album       = db.Column(db.String(100))
    upload_time = db.Column(db.DateTime)

    def __init__(self, filename, filetype, title, artist, album):
        self.song_id     = str(uuid.uuid4()).replace("-", "")
        self.filename    = filename
        self.filetype    = filetype
        self.title       = title
        self.artist      = artist
        self.album       = album
        self.upload_time = datetime.datetime.now()

    def __repr__(self):
        return "<Song %r %r>" % (self.song_id, self.title)