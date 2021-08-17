from datetime import datetime
from datetime import timedelta
from datetime import timezone

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource, abort
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import secret
import os


CONNECT = f"mysql+pymysql://{secret.dbuser}:{secret.dbpass}@{secret.dbhost}/{secret.dbname}?charset=utf8mb4"


# Init app

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['SQLALCHEMY_DATABASE_URI'] = CONNECT
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["JWT_SECRET_KEY"] = "brrijLkcofcJVlwt-Qmd2xM-TXU"  # Change this!
app.config["JWT_COOKIE_SECURE"] = False
# app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=365)
jwt = JWTManager(app)
api = Api(app)
bcrypt = Bcrypt(app)



# INIT db
db = SQLAlchemy(app)

# Init Ma

ma = Marshmallow(app)
