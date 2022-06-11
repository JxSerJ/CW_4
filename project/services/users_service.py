from project.exceptions import ItemNotFound
from project.schemas import UserSchema
from project.services.base import BaseService

user_schema = UserSchema()


class UsersService(BaseService):
    def get_item_by_id(self, pk) -> list:
        user = self.dao.get_by_id(pk)
        if not user:
            raise ItemNotFound
        return user_schema.dump(user)

    def get_user_by_email(self, email: str) -> list:
        user = self.dao.get_by_email(email)
        if not user:
            raise ItemNotFound
        return user_schema.dump(user)

    def update(self, email, data) -> list:
        user = self.dao.get_by_email(email)
        if not user:
            raise ItemNotFound
        return user_schema.dump(self.dao.update(user, data))

    def update_password(self, email, password1, password2):
        user = self.dao.get_by_email(email)
        if not user:
            raise ItemNotFound

