from flask import Flask, session
from flask.ext.restful import Api

from database import db
from api.user import UserApi
from api.request import RequestApi
from api.friends import FriendsApi

app = Flask(__name__)

app.debug = True
app.secret_key = "PolarBearSunset"

# Initialize Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database/prototapes.db'
db.init_app(app)
with app.app_context():
    db.create_all()

# Initialize API
api = Api(app)
api.add_resource(UserApi, '/user')
api.add_resource(FriendsApi, '/friends')
api.add_resource(RequestApi, '/request')


@app.route('/')
def hello():
    return "Hello world"


@app.route('/logout')
def logout():
    session.clear()
    return "Logged out"

if __name__ == '__main__':
    app.run()
