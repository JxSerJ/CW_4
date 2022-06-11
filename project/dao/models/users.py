from project.dao.models import Genre
from project.dao.models.base import BaseMixin
from project.setup_db import db


class User(BaseMixin, db.Model):
    __tablename__ = "users"
    __bind_key__ = "users"

    email = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255))
    surname = db.Column(db.String(255))
    favorite_genre = db.Column(db.ForeignKey(Genre.id))

    def __repr__(self):
        return f"<User '{self.email}'>"
