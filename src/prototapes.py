from flask import Flask
from flask.ext.restful import Api

from database import db
from api.user import UserApi

app = Flask(__name__)


app.debug = True

# Initialize Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database/prototapes.db'
db.init_app(app)
with app.app_context():
    db.create_all()

# Initialize API
api = Api(app)
api.add_resource(UserApi, '/user')



@app.route('/')
def hello():
    return "Hello world"

if __name__ == '__main__':
    app.run()
