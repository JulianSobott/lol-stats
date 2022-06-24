from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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