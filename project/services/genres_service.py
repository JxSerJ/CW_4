from project.exceptions import ItemNotFound
from project.schemas import GenreSchema
from project.services.base import BaseService

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


class GenresService(BaseService):
    def get_item_by_id(self, pk) -> list:
        genre = self.dao.get_by_id(pk)
        if not genre:
            raise ItemNotFound
        return genre_schema.dump(genre)

    def get_all_genres(self) -> list:
        genres = self.dao.get_all()
        return genres_schema.dump(genres)
