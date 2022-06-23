from project.dao.models import User
from project.dao.models.base import BaseMixin
from project.setup_db import db


class Token(BaseMixin, db.Model):
    __tablename__ = "tokens"
    __bind_key__ = "tokens"

    user_id = db.Column(db.ForeignKey(User.id), unique=True)
    email = db.Column(db.ForeignKey(User.email), unique=True)
    access_token = db.Column(db.String, unique=True)
    refresh_token = db.Column(db.String, unique=True)

    def __repr__(self):
        return f"<Token for '{self.email}'>"
