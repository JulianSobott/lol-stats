from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    email = fields.Email(required=True, allow_none=False, error="Invalid mail")
    password = fields.String(validate=validate.Length(min=6, max=20), required=True, error="Invalid password", allow_none=True)


class CompetitorSchema(Schema):
    player_uuid = fields.String(required=True)


class UserSetupSchema(Schema):
    region = fields.Field(load_default="euw")
    player_uuid = fields.String(required=True)


class UserDumpSchema(Schema):
    id = fields.Integer(required=True)
    email = fields.Email(required=True, allow_none=False, error="Invalid mail")
    region = fields.Field()
    player_uuid = fields.String()


class AchievementSchema(Schema):
    name = fields.String(required=True)


user_schema = UserSchema()
competitor_schema = CompetitorSchema()
user_setup_schema = UserSetupSchema()
user_dump_schema = UserDumpSchema()
achievement_schema = AchievementSchema()
