from flask import current_app
from sqlalchemy import desc

from project.dao.base import BaseDAO
from project.dao.models import Movie


class MovieDAO(BaseDAO):
    def get_by_id(self, pk) -> Movie:
        return self._db_session.query(Movie).filter(Movie.id == pk).one_or_none()

    def get_all(self, page: int = None, status: str = None) -> list[Movie]:

        query = self._db_session.query(Movie)

        if status:
            query = query.order_by(desc(Movie.year))
        if page:
            items_per_page = current_app.config["ITEMS_PER_PAGE"]
            offset = page * items_per_page - items_per_page
            query = query.limit(items_per_page).offset(offset)

        return query.all()
