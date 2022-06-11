from marshmallow import fields, Schema


class UserSchema(Schema):
    id = fields.Integer(dump_only=True, required=True)
    email = fields.String(required=True)
    password_hash = fields.String(load_only=True)
    name = fields.String()
    surname = fields.String()
    favorite_genre = fields.String()
