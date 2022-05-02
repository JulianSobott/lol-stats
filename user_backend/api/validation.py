from marshmallow import Schema, fields


class FormSchema(Schema):
    mail = fields.Email(required=True)
    password = fields.String(required=True)


class TokenSchema(Schema):
    token = fields.String(required=True)


class CompetitorSchema(Schema):
    player_uuid = fields.String(required=True)
    token = fields.Nested(TokenSchema())


form_schema = FormSchema()
token_schema = TokenSchema()
competitor_schema = CompetitorSchema()
