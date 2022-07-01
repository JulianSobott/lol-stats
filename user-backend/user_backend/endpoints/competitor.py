from models import db, Competitors, Users
from userToken import token_required
from validation import competitor_schema
import requests
from marshmallow import ValidationError
from flask import request, make_response, jsonify, Blueprint

competitor_blueprint = Blueprint('competitor_blueprint', __name__)


@competitor_blueprint.route('/api/users/<user_id>/competitors/', methods=['GET'])
def get_list_of_competitor(user_id):
        competitors = Competitors.query.filter_by(user_id=user_id).all()

        competitor_output = []
        for competitor in competitors:
            player_response = requests.get(f"https://lol-stats.de/api/players/{competitor.player_uuid}")
            player_stats = player_response.json()

            data = {
                "id": competitor.id,
                "player_uuid": competitor.player_uuid,
                "player_name": player_stats["name"],
                "player_stats": player_stats
            }
            competitor_output.append(data)
        return make_response(jsonify({"status": "success",
                                      "competitors": competitor_output}), 200)


@competitor_blueprint.route('/api/users/<user_id>/competitors/puuids', methods=['GET'])
def get_list_of_competitor_puuids(user_id):
    competitors = Competitors.query.filter_by(user_id=user_id).all()
    competitor_output = list(map(lambda c: c.player_uuid, competitors))
    return make_response(jsonify({"status": "success", "competitors": competitor_output}), 200)


@competitor_blueprint.route('/api/users/<user_id>/competitors', methods=['POST'])
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


@competitor_blueprint.route('/api/users/<user_id>/competitors/<competitor_puuid>', methods=['GET'])
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


@competitor_blueprint.route('/api/users/<user_id>/competitors/<competitor_puuid>', methods=['DELETE'])
@token_required
def delete_competitor(current_user, token, user_id, competitor_puuid):
    if current_user.id == int(user_id):
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
