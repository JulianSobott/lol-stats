from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    email = fields.Email(required=True, allow_none=False, error="Invalid Input")
    password = fields.String(validate=validate.Length(min=6, max=20), required=True, error="Invalid Input", allow_none=True)


class CompetitorSchema(Schema):
    user_id = fields.Integer(required=True)
    player_uuid = fields.String(required=True)


user_schema = UserSchema()
competitor_schema = CompetitorSchema()
