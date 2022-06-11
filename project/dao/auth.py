from project.dao.models import User
from project.dao.base import BaseDAO


class AuthDAO(BaseDAO):

    def create(self, email: str, password_hash: str) -> User:

        new_user = User(
            email=email,
            password_hash=password_hash
        )

        self._db_session.add(new_user)
        self._db_session.commit()

        return new_user

    def get_user_by_email(self, email: str) -> User:
        user = self._db_session.query(User).filter(User.email == email).one_or_none()
        return user

    def update_user_password(self, email: str, new_password_hash: str):
        user = self.get_user_by_email(email)
        user.password_hash = new_password_hash
        self._db_session.add(user)
        self._db_session.commit()
