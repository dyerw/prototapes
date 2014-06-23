from database import db


class Friends(db.Model):
    friend1 = db.Column(db.String(10), db.ForeignKey('user.username'), primary_key=True)
    friend2 = db.Column(db.String(10), db.ForeignKey('user.username'), primary_key=True)

    def __init__(self, friend1, friend2):
        self.friend1 = friend1
        self.friend2 = friend2

    def __repr__(self):
        return "<Friends %r %r>" % (self.friend1, self.friend2)