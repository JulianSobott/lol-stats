from marshmallow import Schema, fields


class UserSchema(Schema):
    email = fields.Email(required=True, allow_none=False, error="Invalid Input")
    password = fields.String(min=6, required=True, error="Invalid Input", allow_none=False)


class TokenSchema(Schema):
    token = fields.String(required=True)


class CompetitorSchema(Schema):
    player_uuid = fields.String(required=True)
    token = fields.Nested(TokenSchema())


user_schema = UserSchema()
token_schema = TokenSchema()
competitor_schema = CompetitorSchema()
