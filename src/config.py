from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import dotenv
import os


dotenv.load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)
login_manager = LoginManager()
login_manager.init_app(app)

user = os.getenv('NAME')
password = os.getenv('PASSWORD')
host = os.getenv('HOST')
port = os.getenv('PORT')
database = os.getenv('DATABASE')
items = [user, password, host, port, database]


url = f'https://cloud-api.yandex.net/v1/disk/public/resources/?public_key='
path = 'https://disk.yandex.ru/d/ZR99TbwXbnvQtQ'

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}/{database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<Article %r' % self.id