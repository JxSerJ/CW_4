import hmac

import jwt
import calendar
from datetime import datetime, timedelta

from flask import current_app
from jwt import DecodeError, ExpiredSignatureError

from project.dao import AuthDAO
from project.dao.models import User
from project.services.base import BaseService
from project.schemas.auth import AuthUserSchema

from project.tools.security import generate_password_digest, generate_password_b64
from project.exceptions import UserNotFound, IncorrectPassword, InvalidTokens

user_created_schema = AuthUserSchema()


class AuthService(BaseService[AuthDAO]):
    def __get_hash(self, password: str) -> str:
        """Generates hash and decodes it into string with UTF-8 decoded characters"""
        password_hash_digest = generate_password_digest(password)
        password_hash_b64 = generate_password_b64(password_hash_digest)

        return password_hash_b64.decode('utf-8')

    def __compare_password_digest(self, password1, password2) -> bool:
        """Compares two passwords. Returns bool as the result"""
        return hmac.compare_digest(password1, password2)

    def __decode_jwt(self, token) -> dict[str, any]:
        """Decodes jwt and returns jwt-payload"""
        token_data = jwt.decode(
            jwt=token,
            key=current_app.config['SECRET_KEY'],
            algorithms=current_app.config['JWT_ALGO']
        )
        return token_data

    def __generate_tokens(self, user: User)  -> dict[str, str]:
        """Generates pair of tokens"""

        data = {
            "email": user.email,
            "id": user.id
        }

        min30 = datetime.utcnow() + timedelta(minutes=current_app.config['TOKEN_EXPIRE_MINUTES'])
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(
            payload=data,
            key=current_app.config['SECRET_KEY'],
            algorithm=current_app.config['JWT_ALGO']
        )

        days130 = datetime.utcnow() + timedelta(days=current_app.config['TOKEN_EXPIRE_DAYS'])
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(
            payload=data,
            key=current_app.config['SECRET_KEY'],
            algorithm=current_app.config['JWT_ALGO']
        )

        tokens = {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

        self.dao.write_tokens(data, tokens)

        return tokens

    def register(self, password: str, email: str) -> AuthUserSchema:
        """Creates new user with email and password"""
        password_hash = self.__get_hash(password)
        new_user = self.dao.create(email=email, password_hash=password_hash)

        return user_created_schema.dump(new_user)

    def login(self, password: str, email: str) -> dict[str, str]:
        """Checks password and if it is correct generates pair of tokens"""
        user = self.dao.get_user_by_email(email=email)
        if user is None:
            raise UserNotFound

        password_hash = self.__get_hash(password)

        if not self.__compare_password_digest(password1=password_hash, password2=user.password_hash):
            raise IncorrectPassword

        return self.__generate_tokens(user)

    def approve_tokens(self, tokens: dict[str, str]) -> dict[str, str]:
        """Decodes access and refresh tokens. If tokens valid but expired the new pair wil be generated.
        If tokens are invalid - InvalidTokens exception will be raised"""
        try:
            self.__decode_jwt(tokens['access_token'])
            self.__decode_jwt(tokens['refresh_token'])
        except DecodeError:
            raise InvalidTokens
        except ExpiredSignatureError:
            user_email = self.__decode_jwt(tokens['refresh_token'])['email']
            user = self.dao.get_user_by_email(email=user_email)
            if user is None:
                raise UserNotFound
            return self.__generate_tokens(user)

    def update_password(self, email, old_password, new_password):
        """Checks if old_password is correct and if so updates password to new_password.
        Otherwise, raises IncorrectPassword exception"""
        user = self.dao.get_user_by_email(email=email)
        if user is None:
            raise UserNotFound

        old_password_hash = self.__get_hash(old_password)

        if not self.__compare_password_digest(password1=old_password_hash, password2=user.password_hash):
            raise IncorrectPassword

        new_password_hash = self.__get_hash(new_password)

        self.dao.update_user_password(email=email, new_password_hash=new_password_hash)
