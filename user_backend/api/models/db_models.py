import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(255), primary_key=True)
    player_uuid = db.Column(db.String(255))
    password = db.Column(db.String(255))
    email = db.Column(db.String(255))


class Competitors(db.Model):
    __tablename__ = 'competitors'
    id = db.Column(db.Integer, primary_key=True)
    user_uid = db.Column(db.String(255))
    player_uuid = db.Column(db.String(255))
    username = db.Column(db.String(255))
