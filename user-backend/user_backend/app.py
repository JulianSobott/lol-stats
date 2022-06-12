import datetime
import os
import time
from functools import wraps
from urllib import response
import requests

import jwt
import schedule
from schedule import every, repeat, run_pending
from flask_cors import CORS
from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError
from werkzeug import security

import config
from validation import user_schema, competitor_schema, user_setup_schema, user_dump_schema, UserDumpSchema, achievement_schema


def create_app():
    flask_app = Flask(__name__)
    CORS(flask_app, origins=['*', 'http://localhost:3000'], allow_headers=['*'], supports_credentials=False)
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    flask_app.url_map.strict_slashes = False
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
    region = db.Column(db.String(20), default="euw")
    competitors = db.relationship('Competitors', backref='user', lazy=True)
    access_token = db.relationship('AccessToken', backref='user', lazy=True)
    favourite_achievement = db.relationship('FavouriteAchievement', backref='user', lazy=True)


class Competitors(db.Model):
    __tablename__ = 'competitors'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    player_uuid = db.Column(db.String(255), nullable=False)


class AccessToken(db.Model):
    __tablename__ = 'access_token'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, nullable=False)


class FavouriteAchievement(db.Model):
    __tablename__ = 'favourite_achievement'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)


def get_token(header):
    if 'Authentication' in request.headers:
        token = request.headers['Authentication']
    else:
        return None

    return token.replace("Bearer ", "")


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = get_token(request.headers)
        if token is None:
            return make_response(jsonify({"status": "error", 'message': 'No Authentication in Header'}), 401)

        if not token:
            return make_response(jsonify({"status": "error", 'message': 'No token'}), 404)
        try:
            api_key = token.replace("Bearer ", "")
            data = jwt.decode(api_key, app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
            current_user = Users.query.filter_by(id=data['user_id']).first()
        except:
            db_token = AccessToken.query.filter_by(token=token).first()
            if db_token is not None:
                db.session.delete(db_token)
                db.session.commit()
            return make_response(jsonify({"status": "error", 'message': 'Token is invalid'}), 400)

        return f(*(current_user, token) + args, **kwargs)

    return decorator


@repeat(every(5).seconds)
def delete_expired_token():
    token_query = AccessToken.query.order_by(AccessToken.created_at).all()
    expired = True
    for token in token_query:
        if expired:
            try:
                data = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
                expired = False
            except:
                db.session.delete(token)
                db.session.commit()
                continue


@app.route('/api/auth/me', methods=['GET'])
@token_required
def get_own_data(current_user, access_token):
    player_stats = {}
    
    try:
        response = requests.get(f"https://lol-stats.de/api/players/{current_user.player_uuid}")
        player_stats = response.json()
    except Exception as exc:
        print(f"Error: {exc}")

    user = Users.query.filter_by(id=current_user.id).first()

    user = {
        "id": user.id,
        "player_uuid": user.player_uuid,
        "email": user.email,
        "token": access_token,
        "region": user.region,
        "player_stats": player_stats,
    }

    return make_response(
        jsonify({"status": "success", "user": user}),
        200)


@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return make_response(jsonify({"status": "error", "message": "No input data provided"}), 400)
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

                user = user_dump_schema.dump(user)

                return make_response(
                    jsonify({"status": "success", "user": user, "token": access_token}), 200)
            else:
                return make_response(jsonify({"status": "error", "message": "Wrong password"}), 400)
        else:
            return make_response(jsonify({"status": "error", "message": "No password"}), 400)
    else:
        return make_response(jsonify({"status": "error", "message": "User not found"}), 404)


@app.route('/api/token/info', methods=['GET'])
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
        db_token = get_token(request.headers)
        if db_token is None:
            return make_response(jsonify({"status": "error", 'message': 'No Authentication in Header'}), 401)

        db_token = AccessToken.query.filter_by(token=db_token).first()
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
        return make_response(jsonify({"status": "error", "message": "No input data provided"}), 400)
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
        user = user_dump_schema.dump(user)
        return make_response(
            jsonify({"status": "success",
                     "user": user}), 200)
    else:
        return make_response(
            jsonify({"status": "error", "message": "Account with given mail already exists"}),
            409)


@app.route('/api/auth/delete', methods=['DELETE'])
@token_required
def delete_user(current_user, token):
    user = Users.query.filter_by(id=current_user.id).first()
    if user is None:
        return make_response(jsonify({"status": "error",
                                      "message": "User not found"}), 404)

    AccessToken.query.filter_by(user_id=current_user.id).delete()
    Competitors.query.filter_by(user_id=current_user.id).delete()

    db.session.delete(user)
    db.session.commit()

    return make_response(jsonify({"status": "success",
                                  "message": "No content",
                                  }), 200)


@app.route('/api/users/<user_id>', methods=['PUT'])
@token_required
def put_player_uuid(current_user, access_token, user_id):
    if current_user.id == int(user_id):
        user = Users.query.filter_by(id=current_user.id).first()
        data = request.get_json()

        if user is not None:
            if not data:
                return make_response(jsonify({"status": "error", "message": "No input data provided"}), 400)
            try:
                data = user_setup_schema.load(data)
            except ValidationError as err:
                return make_response(jsonify({"status": "error", "message": err.messages}), 400)

            if "region" in data:
                if not data["region"]:
                    user.region = "euw"
                else:
                    user.region = data["region"]
            if "player_uuid" in data:
                user.player_uuid = data["player_uuid"]

            db.session.commit()

            user = user_dump_schema.dump(user)

            return make_response(
                jsonify({
                    "user": user,
                    "token": access_token,
                    "status": "success"
                }), 200)
        else:
            return make_response(jsonify({"status": "error", "message": "User not found"}), 404)
    else:
        return make_response(jsonify({"status": "error",
                                      "message": "Not authorized"}), 401)


@app.route('/api/users/<user_id>', methods=['GET'])
def get_player(user_id: int):
    user = Users.query.filter_by(id=user_id).first()
    if user is not None:
        user_dump = UserDumpSchema(exclude=["email"]).dump(user)
        return make_response(jsonify(user_dump), 200)
    
    return make_response(jsonify({"status": "error", "message": "User not found"}), 404)


@app.route('/api/users/<user_id>/competitors/', methods=['GET'])
@token_required
def get_list_of_competitor(current_user, token, user_id):
        competitors = Competitors.query.filter_by(user_id=user_id).all()

        competitor_output = []
        for competitor in competitors:
            if current_user.player_uuid is not None:
                player_response = requests.get(f"https://lol-stats.de/api/players/{competitor.player_uuid}")
                player_stats = player_response.json()

                data = {
                    "id": competitor.id,
                    "player_uuid": competitor.player_uuid,
                    "player_name": player_stats.player_name,
                    "player_stats": {}
                }
                competitor_output.append(data)
        return make_response(jsonify({"status": "success",
                                      "competitors": competitor_output}), 200)


@app.route('/api/users/<user_id>/competitors', methods=['POST'])
@token_required
def add_competitor(current_user, token, user_id):
    if current_user.id == int(user_id):
        data = request.get_json()
        if not data:
            return make_response(jsonify({"status": "error", "message": "No input data provided"}), 400)
        try:
            data = competitor_schema.load({"player_uuid": data["player_uuid"]})
        except ValidationError as err:
            return make_response(jsonify({"status": "error", "message": err.messages}), 400)

        if Competitors.query.filter_by(user_id=user_id, player_uuid=data["player_uuid"]).first() is None:
            user = Users.query.filter_by(id=current_user.id).first()
            if user.player_uuid == data["player_uuid"]:
                return make_response(jsonify({"status": "error", "message": "You can not add yourself as a competitor!"}),
                                 400)
            username = None

            player_response = requests.get(f"https://lol-stats.de/api/players/{data['player_uuid']}")
            player_stats = player_response.json()
            if player_stats is not None:
                competitor = Competitors(user_id=user_id, player_uuid=data["player_uuid"])
                db.session.add(competitor)
                db.session.commit()
                return make_response(
                    jsonify({"status": "success",
                             "message": "No content"}), 200)
            else:
                return make_response(
                    jsonify(
                        {"status": "error", "message": "No such competitor found"}),
                    400)
        else:
            return make_response(
                jsonify(
                    {"status": "error", "message": "Competitorship already exists"}),
                409)
    else:
        return make_response(jsonify({"status": "error",
                                      "message": "Not authorized"}), 401)


@app.route('/api/users/<user_id>/competitors/<competitor_puuid>', methods=['GET'])
@token_required
def get_competitor(current_user, token, user_id, competitor_puuid):
    if current_user.id == int(user_id):
        competitor = Competitors.query.filter_by(user_id=current_user.id, player_uuid=competitor_puuid).first()
        if competitor is None:
            return make_response(jsonify({"status": "error",
                                        "message": "Competitor not found in your competitorship"}), 404)

        player_stats = {}
        if competitor_puuid is not None:
            player_response = requests.get(f"https://lol-stats.de/api/players/{competitor_puuid}")
            player_stats = player_response.json()

        competitor_data = {
            "id": competitor.id,
            "player_uuid": competitor.player_uuid,
                "username": player_stats.name,
                "player_stats": player_stats
        }

        return make_response(jsonify({"status": "success",
                                    "competitors": competitor_data}), 200)
    else:
        return make_response(jsonify({"status": "error",
                                      "message": "Not authorized"}), 401)


@app.route('/api/users/<user_id>/competitors/<competitor_puuid>', methods=['DELETE'])
@token_required
def delete_competitor(current_user, token, user_id, competitor_puuid):
    if current_user.id == user_id:
        competitor = Competitors.query.filter_by(user_id=user_id, player_uuid=competitor_puuid).first()
        if competitor is None:
            return make_response(jsonify({"status": "error",
                                        "message": "Competitor not found in your competitorship"}), 404)

        db.session.delete(competitor)
        db.session.commit()

        return make_response(jsonify({"status": "success",
                                    "message": "No content",
                                    }), 200)
    else:
        return make_response(jsonify({"status": "error",
                                      "message": "Not authorized"}), 401)


@app.route('/api/users/<user_id>/achievements', methods=['GET'])
def get_achievements(current_user, token, user_id):
    if current_user.id == int(user_id):
        db_achievement = FavouriteAchievement.query.filter_by(user_id=user_id).all()
        achievements = []
        for item in db_achievement:
            if item.name is not None:
                achievements.append(item.name)
        return make_response(jsonify({"status": "success",
                                      "achievements": achievements}), 200)
    else:
        return make_response(jsonify({"status": "error",
                                      "message": "Not authorized"
                                      }), 401)


@app.route('/api/users/<user_id>/achievements', methods=['POST'])
@token_required
def add_achievements(current_user, token, user_id):
    if current_user.id == int(user_id):
        data = request.get_json()
        if not data:
            return make_response(jsonify({"status": "error", "message": "No input data provided"}), 400)
        try:
            data = achievement_schema.load({"name": data["name"]})
        except ValidationError as err:
            return make_response(jsonify({"status": "error", "message": err.messages}), 400)

        db_achievement = FavouriteAchievement.query.filter_by(user_id=user_id, name=data["name"]).first()

        if db_achievement is not None:
            return make_response(jsonify({"status": "error",
                                          "message": "Achievement already set as favourite"}), 400)

        user = Users.query.filter_by(id=user_id).first()
        if user is not None:
            db_achievement = FavouriteAchievement(user_id=user_id, name=data["name"])
            db.session.add(db_achievement)
            db.session.commit()

        return make_response(
            jsonify({"status": "success",
                     "message": "No Content"}), 200)
    else:
        return make_response(jsonify({"status": "error",
                                      "message": "Not authorized"}), 401)


@app.route('/api/users/<user_id>/achievements/<achievement_name>', methods=['DELETE'])
@token_required
def delete_achievement(current_user, token, user_id, achievement_name):
    if current_user.id == int(user_id):
        achievement = FavouriteAchievement.query.filter_by(user_id=user_id, name=achievement_name).first()
        if achievement is None:
            return make_response(jsonify({"status": "error",
                                          "message": "Achievement not found"}), 404)

        db.session.delete(achievement)
        db.session.commit()

        return make_response(jsonify({"status": "success",
                                      "message": "No content",
                                      }), 200)
    else:
        return make_response(jsonify({"status": "error",
                                      "message": "Not authorized"}), 401)


if __name__ == '__main__':
    app.run(debug=True)
    while True:
        # Checks whether a scheduled task
        # is pending to run or not
        schedule.run_pending()
        time.sleep(1)
