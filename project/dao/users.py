from project.dao.base import BaseDAO
from project.dao.models import User


class UserDAO(BaseDAO):
    def get_by_id(self, pk: int) -> User:
        user: User = self._db_session.query(User).filter(User.id == pk).one_or_none()
        return user

    def get_by_email(self, email: str) -> User:
        user: User = self._db_session.query(User).filter(User.email == email).one_or_none()
        return user

    def update(self, email, data):
        user = self.get_by_email(email)

        for k, v in data.items():
            setattr(user, k, v)

        self._db_session.add(user)
        self._db_session.commit()
