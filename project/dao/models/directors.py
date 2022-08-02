from project.dao.models.base import BaseMixin
from project.setup_db import db


class Director(BaseMixin, db.Model):
    __tablename__ = "directors"
    # __bind_key__ = "main"

    name = db.Column(db.String(200), unique=True, nullable=False)

    def __repr__(self):
        return f"<Director '{self.name.title()}'>"
