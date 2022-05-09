from marshmallow import Schema, fields


class UserSchema(Schema):
    email = fields.Email(required=True, allow_none=False, error="Invalid Input")
    password = fields.String(min=6, required=True, error="Invalid Input", allow_none=False)


class CompetitorSchema(Schema):
    user_id = fields.Integer(required=True)
    player_uuid = fields.String(required=True)


user_schema = UserSchema()
competitor_schema = CompetitorSchema()
