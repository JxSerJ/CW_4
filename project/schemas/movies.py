from marshmallow import fields, Schema
from project.schemas import GenreSchema, DirectorSchema


class MovieSchema(Schema):
    id = fields.Integer(dump_only=True, required=True)
    title = fields.String(required=True)
    description = fields.String(required=True)
    trailer = fields.String(required=True)
    year = fields.Integer(required=True)
    rating = fields.Float(required=True)
    genre = fields.Nested(GenreSchema)
    director = fields.Nested(DirectorSchema)

    # genre_id = fields.Integer(required=True)
    # director_id = fields.Integer(required=True)
