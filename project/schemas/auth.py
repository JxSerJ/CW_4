from marshmallow import fields, Schema

from project.schemas import UserSchema


class AuthUserSchema(Schema):
    id = fields.Int()
    email = fields.Str(required=True)
    password = fields.Str(required=True)


class AuthRegisterData(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)


class AuthLoginSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)


class TokenSchema(Schema):
    id = fields.Integer(dump_only=True, required=True)
    email = fields.Nested(UserSchema)
    access_token = fields.String()
    refresh_token = fields.String()
