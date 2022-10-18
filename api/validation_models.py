from marshmallow import Schema, fields


class UserSchema(Schema):
    user_name = fields.Str(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Email(required=True)


class NewUserSchema(Schema):
    user_name = fields.Str(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class SearchSchema(Schema):
    user_name = fields.Str(required=True)
    search_city = fields.Str(required=True)
    observation_time = fields.Str(required=True)
    weather = fields.Str(required=True)
    temperature_celicius = fields.Float(required=True)
    temperature_celicius_indoor = fields.Float(required=True)
    humidity = fields.Float(required=True)
    humidity_indoor = fields.Float(required=True)


class LoginSchema(Schema):
    user_name = fields.Str(required=True)
    password = fields.Str(required=True)


new_user_schema = NewUserSchema()
user_schema = UserSchema()
search_shema = SearchSchema()
login_schema = LoginSchema()
