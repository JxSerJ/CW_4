from project.exceptions import ItemNotFound
from project.schemas import MovieSchema
from project.services.base import BaseService

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


class MoviesService(BaseService):
    def get_item_by_id(self, pk):
        movie = self.dao.get_by_id(pk)
        if not movie:
            raise ItemNotFound
        return movie_schema.dump(movie)

    def get_all_movies(self):
        movies = self.dao.get_all()
        return movies_schema.dump(movies)
