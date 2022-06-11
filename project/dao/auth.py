from project.dao.models import User, Token
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

    def write_tokens(self, data, tokens: dict):

        token_entry = self._db_session.query(Token).filter(Token.email == data["email"]).one_or_none()
        if token_entry is None:
            token_entry = Token(
                user_id=data["id"],
                email=data["email"],
                access_token=tokens["access_token"],
                refresh_token=tokens["refresh_token"]
            )
        else:
            data_to_update = {"user_id": data["id"],
                              "email": data["email"],
                              "access_token": tokens["access_token"],
                              "refresh_token": tokens["refresh_token"]}
            for k, v in data_to_update.items():
                setattr(token_entry, k, v)

        self._db_session.add(token_entry)
        self._db_session.commit()
