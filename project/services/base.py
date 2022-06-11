from typing import TypeVar, Generic

from project.dao.base import BaseDAO

type_var = TypeVar('type_var', bound=BaseDAO)


class BaseService(Generic[type_var]):
    def __init__(self, dao: type_var):
        self.dao = dao
