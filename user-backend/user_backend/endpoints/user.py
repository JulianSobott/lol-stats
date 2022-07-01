import datetime
from models import Users, AccessToken, Competitors, db
from userToken import token_required, get_token
from validation import user_schema, user_setup_schema, user_dump_schema, UserDumpSchema
import requests

from marshmallow import ValidationError
from sentry_sdk import capture_exception
from werkzeug import security

import jwt
import config
from flask import request, make_response, jsonify, Blueprint

user_blueprint = Blueprint('user_blueprint', __name__)


@user_blueprint.route('/api/auth/me', methods=['GET'])
@token_required
def get_own_data(current_user, access_token):
    player_stats = {}

    try:
        response = requests.get(f"https://lol-stats.de/api/players/{current_user.player_uuid}")
        player_stats = response.json()
    except Exception as exc:
        capture_exception(exc)
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


@user_blueprint.route('/api/auth/login', methods=['POST'])
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
                    {'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},
                    config.JWT_SECRET_KEY, "HS256")
                db_token = AccessToken(user_id=user.id, token=access_token, created_at=datetime.datetime.utcnow(),
                                       updated_at=datetime.datetime.utcnow() + datetime.timedelta(minutes=60))
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


@user_blueprint.route('/api/token/info', methods=['GET'])
@token_required
def verify_token(current_user, access_token):
    if current_user is not None:
        return make_response(
            jsonify({"status": "success", "id": current_user.id, "player_uuid": current_user.player_uuid,
                     "email": current_user.email, "token": access_token}), 200)
    else:
        return make_response(jsonify({"status": "error", "message": "Invalid token"}), 400)


@user_blueprint.route('/api/auth/logout', methods=['POST'])
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


@user_blueprint.route('/api/auth/register', methods=['POST'])
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


@user_blueprint.route('/api/auth/delete', methods=['DELETE'])
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


@user_blueprint.route('/api/users/<user_id>', methods=['PUT'])
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


@user_blueprint.route('/api/users/<user_id>', methods=['GET'])
def get_player(user_id: int):
    user = Users.query.filter_by(id=user_id).first()
    if user is not None:
        user_dump = UserDumpSchema(exclude=["email"]).dump(user)
        return make_response(jsonify(user_dump), 200)

    return make_response(jsonify({"status": "error", "message": "User not found"}), 404)
