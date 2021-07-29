from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource, abort
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import secret


CONNECT = f"mysql+pymysql://{secret.dbuser}:{secret.dbpass}@{secret.dbhost}/{secret.dbname}"

# Init app

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['SQLALCHEMY_DATABASE_URI'] = CONNECT
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "brrijLkcofcJVlwt-Qmd2xM-TXU"  # Change this!
jwt = JWTManager(app)
api = Api(app)
bcrypt = Bcrypt(app)



# INIT db
db = SQLAlchemy(app)

# Init Ma

ma = Marshmallow(app)

