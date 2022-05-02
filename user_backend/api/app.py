import os
import database
import config
import validation
from models.db_models import db, Users
from flask import Flask, request, make_response, jsonify
from werkzeug import security
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token, JWTManager


def create_app():
    flask_app = Flask(__name__)
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    flask_app.app_context().push()
    db.init_app(flask_app)  # link api to db
    db.create_all()
    flask_app.config["JWT_SECRET_KEY"] = config.JWT_SECRET_KEY
    JWTManager(flask_app)
    return flask_app


app = create_app()
salt = os.urandom(32)


@app.route('/hello', methods=['GET'])
def hello_world():
    return 'Hello World!'


@app.route('/api/users/{user}', methods=['POST'])
def getUser():
    return 'New user registered'


@app.route('/api/auth/me', methods=['GET'])
def ownData():
    return 'New user registered'


@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}, 400)
    try:
        data = validation.form_schema.load(data)
    except ValidationError as err:
        return err.messages, 422
    user = database.get_instance(Users, data["email"])
    if user:
        if user.password:
            hashed_pw = security.generate_password_hash(data["password"])
            if security.check_password_hash(hashed_pw, user.password):
                access_token = create_access_token(identity=user.email)
                return make_response(jsonify({"user": user, "token": access_token}), 200)
            else:
                return make_response(jsonify({"message": "Wrong password"}), 400)
        else:
            return make_response(jsonify({"message": "No password given"}), 400)
    else:
        return make_response(jsonify({"message": "Invalid input"}), 400)


@app.route('/api/auth/logout', methods=['POST'])
def logout():
    return 'User logged out'


@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}, 400)
    try:
        data = validation.form_schema.load(data)
    except ValidationError as err:
        return err.messages, 422
    hashed_pw = security.generate_password_hash(data["password"])
    if not database.get_instance(Users, data["email"]):
        database.add_instance(Users, mail=data["email"], password=hashed_pw)
        return make_response(jsonify({"email": data["email"]}), 200)


if __name__ == '__main__':
    app.run(debug=True)
