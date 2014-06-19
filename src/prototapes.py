from flask import Flask

from database import db

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database/prototapes.db'
db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/')
def hello():
    return "Hello world"

if __name__ == '__main__':
    app.run()
