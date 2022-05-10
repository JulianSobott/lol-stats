import datetime
import os
from functools import wraps

import jwt
from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError
from werkzeug import security

import config
from validation import user_schema, competitor_schema


def create_app():
    flask_app = Flask(__name__)
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
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
    region = db.Column(db.String(20), default="EUW")
    competitors = db.relationship('Competitorship', backref='user', lazy=True)
    access_token = db.relationship('token', backref='user', lazy=True)


class Competitors(db.Model):
    __tablename__ = 'competitors'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    player_uuid = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)


class AccessToken(db.Model):
    __tablename__ = 'access_token'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, nullable=False)


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

        return f(*(current_user, token) + args, **kwargs)

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
    player_stats = {}

    competitors = Competitors.query.filter_by(user_id=current_user.id).all()
    competitor_output = []

    for competitor in competitors:
        data = {
            "id": competitor.id,
            "player_uuid": competitor.player_uuid,
            "username": competitor.username
        }
        competitor_output.append(data)

    return make_response(
        jsonify({"status": "success", "User": user, "player_stats": player_stats, "competitors": competitor_output}),
        200)


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
                db_token = AccessToken(user_id=user.id, token=access_token, created_at=datetime.datetime.utcnow(),
                                       updated_at=datetime.datetime.utcnow() + datetime.timedelta(minutes=45))
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


@app.route('/api/token/token-id', methods=['GET'])
@token_required
def verify_token(current_user, access_token):
    if current_user is not None:
        return make_response(
            jsonify({"status": "success", "id": current_user.id, "player_uuid": current_user.player_uuid,
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
        user = Users.query.filter_by(email=data["email"]).first()
        return make_response(
            jsonify({"status": "success",
                     "id": user.id,
                     "player_uuid": user.player_uuid,
                     "email": user.email}), 200)
    else:
        return make_response(
            jsonify({"status": "error", "message": "Account with given mail already exists"}),
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
        return make_response(jsonify({"status": "error", "message": "User not found"}), 404)


@app.route('/api/users/<user_id>/competitors/', methods=['GET', 'POST'])
@token_required
def get_list_of_or_add_competitor(current_user, token, user_id):
    if request.method == "GET":

        competitors = Competitors.query.filter_by(user_id=user_id).all()

        competitor_output = []
        for competitor in competitors:
            # TODO make request to player endpoint :get competitors ingame data

            data = {
                "id": competitor.id,
                "player_uuid": competitor.player_uuid,
                "username": competitor.username,
                "player_stats": {}
            }
            competitor_output.append(data)
        return make_response(jsonify({"status": "success",
                                      "competitors": competitor_output}), 200)

    elif request.method == "POST":

        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No input data provided"}, 400)
        try:
            data = competitor_schema.load({"user_id": user_id, "player_uuid": data["player_uuid"]})
        except ValidationError as err:
            return make_response(jsonify({"status": "error", "message": err.messages}), 400)

        if Competitors.query.filter_by(user_id=user_id, player_uuid=data["player_uuid"]).first() is None:
            username = None
            # TODO get username of data["player_uuid"] from player endpoint
            username = "mockUsername"
            if username is not None:
                competitor = Competitors(user_id=user_id, player_uuid=data["player_uuid"], username=username)
                db.session.add(competitor)
                db.session.commit()
                return make_response(
                    jsonify({"status": "success",
                             "message": "No content"}), 200)
            else:
                return make_response(jsonify({"status": "error", "message": "Competitor not found"}), 404)
        else:
            return make_response(
                jsonify(
                    {"status": "error", "message": "Competitorship already exists"}),
                409)


@app.route('/api/users/>user_id>/competitors/<competitor_puuid>', methods=['GET, DELETE'])
@token_required
def get_or_delete_competitor(current_user, token, user_id, competitor_puuid):
    competitor = Competitors.query.filter_by(user_id=user_id, player_uuid=competitor_puuid).first()
    if competitor is None:
        return make_response(jsonify({"status": "error",
                                      "message": "Competitor not found in your competitorship"}), 404)

    if request.method == "GET":

        # TODO make request to player endpoint :get competitors ingame data

        competitor_data = {
            "id": competitor.id,
            "player_uuid": competitor.player_uuid,
            "username": competitor.username,
            "player_stats": {}
        }

        return make_response(jsonify({"status": "success",
                                      "competitors": competitor_data}), 200)

    elif request.method == "DELETE":

        db.session.delete(competitor)
        db.session.commit()

    return make_response(jsonify({"status": "success",
                                  "message": "No content",
                                  }), 200)


if __name__ == '__main__':
    app.run(debug=True)
