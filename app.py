from flask import Flask, request, jsonify
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from Model.model import Visitor


app = Flask(__name__)
CORS(app, supports_credentials=True)
api = Api(app)

# Setup the Flask-JWT-Extended extension
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "brrijLkcofcJVlwt-Qmd2xM-TXU"  # Change this!
jwt = JWTManager(app)

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "test" or password != "test":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(username=current_user), 200


@app.route('/create', methods=["POST"])
def creation():
    username = request.json.get("username", None)
    tel = request.json.get("tel", None)
    status = request.json.get("status", None)
    password = request.json.get("password", None)
    visitor = Visitor(username=username, tel=tel, password=password, status=status)
    visitor.create()
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


if __name__ == "__main__":
    app.run()

