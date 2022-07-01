from models import db, FavouriteAchievement, Users
from userToken import token_required
from validation import achievement_schema
from marshmallow import ValidationError
from flask import request, make_response, jsonify, Blueprint

achievement_blueprint = Blueprint('achievement_blueprint', __name__)


@achievement_blueprint.route('/api/users/<user_id>/achievements', methods=['GET'])
def get_achievements(user_id):
    db_achievement = FavouriteAchievement.query.filter_by(user_id=user_id).all()
    achievements = []
    for item in db_achievement:
        if item.name is not None:
            achievements.append(item.name)
    return make_response(jsonify({"status": "success",
                                    "achievements": achievements}), 200)


@achievement_blueprint.route('/api/users/<user_id>/achievements', methods=['POST'])
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


@achievement_blueprint.route('/api/users/<user_id>/achievements/<achievement_name>', methods=['DELETE'])
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
