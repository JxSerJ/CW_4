from project.exceptions import ItemNotFound
from project.schemas import DirectorSchema
from project.services.base import BaseService

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


class DirectorsService(BaseService):
    def get_item_by_id(self, pk):
        director = self.dao.get_by_id(pk)
        if not director:
            raise ItemNotFound
        return director_schema.dump(director)

    def get_all_directors(self):
        directors = self.dao.get_all()
        return directors_schema.dump(directors)
