from project.dao import GenreDAO, DirectorDAO, MovieDAO


class BaseService:
    def __init__(self, dao: [GenreDAO, DirectorDAO, MovieDAO]):
        self.dao = dao
