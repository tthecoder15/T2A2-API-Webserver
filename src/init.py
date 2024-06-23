from os import environ
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = environ.get("JWT_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DB_URI")
app.json.sort_keys=False

class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
db.init_app(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
