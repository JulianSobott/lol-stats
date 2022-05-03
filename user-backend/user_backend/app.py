import os
import config
from validation import user_schema
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, make_response, jsonify
from werkzeug import security
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token, JWTManager


def create_app():
    flask_app = Flask(__name__)
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    flask_app.app_context().push()
    db.init_app(flask_app)
    flask_app.config["JWT_SECRET_KEY"] = config.JWT_SECRET_KEY
    JWTManager(flask_app)
    return flask_app


db = SQLAlchemy()
app = create_app()
salt = os.urandom(32)


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    player_uuid = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))


class Competitors(db.Model):
    __tablename__ = 'competitors'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_uid = db.Column(db.String(255))
    player_uuid = db.Column(db.String(255))
    username = db.Column(db.String(255))


@app.route('/hello', methods=['GET'])
def hello_world():
    return 'Hello World!'


@app.route('/api/users/{user}', methods=['POST'])
def get_user():
    return 'New user registered'


@app.route('/api/auth/me', methods=['GET'])
def get_own_data():
    return 'New user registered'


@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No input data provided"}, 400)
    try:
        data = user_schema.load(data)
    except ValidationError as err:
        return make_response(jsonify({"message": err.messages}), 400)
    user = Users.query.filter_by(email=data["email"]).first()
    if user is not None:
        if user.password is not None:
            hashed_pw = security.generate_password_hash(data["password"])
            if security.check_password_hash(hashed_pw, user.password):
                access_token = create_access_token(identity=user.email)
                return make_response(jsonify({"status": "success", "user": user.email, "token": access_token}), 200)
            else:
                return make_response(jsonify({"status": "error", "message": "Wrong password"}), 400)
        else:
            return make_response(jsonify({"status": "error", "message": "No password given"}), 400)
    else:
        return make_response(jsonify({"status": "error", "message": "Invalid input"}), 400)


@app.route('/api/auth/logout', methods=['POST'])
def logout():
    return 'User logged out'


@app.route('/api/auth/register', methods=['POST', 'DELETE'])
def register():
    data = request.get_json()
    print(data)
    if not data:
        return jsonify({"status": "error", "message": "No input data provided"}, 400)
    try:
        data = user_schema.load(data)
    except ValidationError as err:
        print(err.messages)
        return make_response(jsonify({"status": "error", "message": err.messages}), 400)
    hashed_pw = security.generate_password_hash(data["password"])
    if Users.query.filter_by(email=data["email"]).first() is None:
        usr = Users(email=data["email"], password=hashed_pw)
        db.session.add(usr)
        db.session.commit()
        return make_response(
            jsonify({"status": "success", "message": "Successfully created account", "email": data["email"]}), 200)
    else:
        return make_response(
            jsonify({"status": "error", "message": "Account with given mail already exists", "email": data["email"]})
            , 409)


if __name__ == '__main__':
    app.run(debug=True)
