from functools import wraps

import jwt
from schedule import every, repeat
from flask import request, make_response, jsonify

from models import db, Users, AccessToken
import config


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
            data = jwt.decode(api_key, config.JWT_SECRET_KEY, algorithms=["HS256"])
            current_user = Users.query.filter_by(id=data['user_id']).first()
        except jwt.ExpiredSignatureError:
            db_token = AccessToken.query.filter_by(token=token).first()
            if db_token is not None:
                db.session.delete(db_token)
                db.session.commit()
            return make_response(jsonify({"status": "error", 'message': 'Token is invalid'}), 400)

        return f(*(current_user, token) + args, **kwargs)

    return decorator


@repeat(every(60).minutes)
def delete_expired_token():
    token_query = AccessToken.query.order_by(AccessToken.created_at).all()
    for token in token_query:
        try:
            jwt.decode(token, config.JWT_SECRET_KEY, algorithms=["HS256"])
            break
        except jwt.ExpiredSignatureError:
            db.session.delete(token)
            db.session.commit()
            continue
