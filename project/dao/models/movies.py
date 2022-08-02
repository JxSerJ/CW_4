from project.dao.models.base import BaseMixin
from project.setup_db import db


class Movie(BaseMixin, db.Model):
    __tablename__ = "movies"
    # __bind_key__ = "main"

    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text())
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer())
    rating = db.Column(db.Float())
    genre_id = db.Column(db.Integer(), db.ForeignKey('genres.id'))
    director_id = db.Column(db.Integer(), db.ForeignKey('directors.id'))

    genre = db.relationship('Genre')
    director = db.relationship('Director')

    def __repr__(self):
        return f"<Movie '{self.title.title()}'>"
