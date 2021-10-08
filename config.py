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
import boto3




CONNECT = f"mysql+pymysql://{secret.dbuser}:{secret.dbpass}@{secret.dbhost}/{secret.dbname}?charset=utf8mb4"

# S3_BUCKET_KEY = "AKIAYMXWVHOCFUJ7HGPJ"
# S3_BUCKET_SECRET = "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"

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
# s3 = boto3.client("s3",
#             region_name="us-east-2",
#             aws_access_key_id=S3_BUCKET_KEY,
#             aws_secret_access_key=S3_BUCKET_SECRET,
#            )



# INIT db
db = SQLAlchemy(app)

# Init Ma

ma = Marshmallow(app)
