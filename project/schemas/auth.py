from marshmallow import fields, Schema


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
