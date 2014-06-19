from database import db


class Request(db.Model):
    requester = db.Column(db.String(10), db.ForeignKey('user.username'), primary_key=True)
    requestee = db.Column(db.String(10), db.ForeignKey('user.username'), primary_key=True)

    def __init__(self, requester, requestee):
        self.requester = requester
        self.requestee = requestee

    def __repr__(self):
        return "<Request %r %r>" % (self.requester, self.requestee)