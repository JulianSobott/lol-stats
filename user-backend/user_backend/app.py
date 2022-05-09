import os

from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError
from werkzeug import security

import config
import jwt
from functools import wraps
import datetime
from validation import user_schema


def create_app():
    flask_app = Flask(__name__)
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
    # flask_app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:password@localhost:5432/userbackend"
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    flask_app.app_context().push()
    db.init_app(flask_app)
    flask_app.config["JWT_SECRET_KEY"] = config.JWT_SECRET_KEY
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
    user_id = db.Column(db.String(255))
    player_uuid = db.Column(db.String(255))
    username = db.Column(db.String(255))


class AccessToken(db.Model):
    __tablename__ = 'access_token'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(255))
    token = db.Column(db.String(255))
    created_at = db.Column(db.TIMESTAMP)
    updated_at = db.Column(db.TIMESTAMP)


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({"status": "error", 'message': 'No token'}, 404)
        try:
            data = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
            current_user = Users.query.filter_by(id=data['user_id']).first()
        except:
            return jsonify({'message': 'Token is invalid'}, 400)

        return f(current_user, token, *args, **kwargs)

    return decorator


@app.route('/api/auth/me', methods=['GET'])
@token_required
def get_own_data(current_user, access_token):
    user = {
        "id": current_user.id,
        "player_uuid": current_user.player_uuid,
        "email": current_user.email,
        "token": access_token
    }

    # TODO implement call to player endpoint and retrieve player data

    competitors = Competitors.query.filter_by(user_id=current_user.id).all()
    competitor_output = []

    for competitor in competitors:
        data = {
            "id": competitor.id,
            "player_uuid": competitor.player_uuid,
            "username": competitor.username
        }
        competitor_output.append(data)

    return make_response(jsonify({"status": "success", "User": user, "competitors": competitor_output}), 200)


@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No input data provided"}, 400)
    try:
        data = user_schema.load(data)
    except ValidationError as err:
        return make_response(jsonify({"status": "error", "message": err.messages}), 400)

    user = Users.query.filter_by(email=data["email"]).first()

    if user is not None:
        if user.password is not None:
            if security.check_password_hash(user.password, data["password"]):
                access_token = jwt.encode(
                    {'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=45)},
                    app.config['JWT_SECRET_KEY'], "HS256")
                db_token = AccessToken(user_id=user.id, token=access_token, created_at=datetime.datetime.utcnow(), updated_at=datetime.datetime.utcnow() + datetime.timedelta(minutes=45))
                db.session.add(db_token)
                db.session.commit()
                return make_response(jsonify({"status": "success", "id": user.id, "player_uuid": user.player_uuid,
                                              "email": user.email, "token": access_token}), 200)
            else:
                return make_response(jsonify({"status": "error", "message": "Invalid Input"}), 400)
        else:
            return make_response(jsonify({"status": "error", "message": "Invalid Input"}), 400)
    else:
        return make_response(jsonify({"status": "error", "message": "User not found"}), 404)


@app.route('/api/auth/token', methods=['GET'])
@token_required
def verify_token(current_user, access_token):
    if current_user is not None:
        return make_response(jsonify({"status": "success", "id": current_user.id, "player_uuid": current_user.player_uuid,
                                      "email": current_user.email, "token": access_token}), 200)
    else:
        return make_response(jsonify({"status": "error", "message": "Invalid token"}), 400)


@app.route('/api/auth/logout', methods=['POST'])
def logout():
    db_token = AccessToken.query.filter_by(token=request.headers['token']).first()
    if db_token is not None:
        db.session.delete(db_token)
        db.session.commit()
        return make_response(jsonify({"status": "success", "message": "Successfully logged out"}), 200)
    else:
        return make_response(jsonify({"status": "error", "message": "Session already expired"}), 400)


@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No input data provided"}, 400)
    try:
        data = user_schema.load(data)
    except ValidationError as err:
        return make_response(jsonify({"status": "error", "message": err.messages}), 400)

    hashed_pw = security.generate_password_hash(password=data["password"])

    if Users.query.filter_by(email=data["email"]).first() is None:
        usr = Users(email=data["email"], password=hashed_pw)
        db.session.add(usr)
        db.session.commit()
        return make_response(
            jsonify({"status": "success", "message": "Successfully created account", "email": data["email"]}), 200)
    else:
        return make_response(
            jsonify({"status": "error", "message": "Account with given mail already exists", "email": data["email"]}),
            409)


@app.route('/api/users/<player_uuid>', methods=['PUT'])
@token_required
def put_player_uuid(current_user, access_token, player_uuid):
    user = Users.query.filter_by(id=current_user.id).first()

    if user is not None:
        user.player_uuid = player_uuid
        db.session.commit()
        return make_response(
            jsonify({"status": "success",
                     "message": "Successfully put ingame user id",
                     "id": current_user.id,
                     "player_uuid": current_user.player_uuid,
                     "email": current_user.email,
                     "token": access_token}), 200)
    else:
        return make_response(
            jsonify({"status": "error", "message": "User not found"}), 404)


if __name__ == '__main__':
    app.run(debug=True)
