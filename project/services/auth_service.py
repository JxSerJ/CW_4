import hmac

import jwt
import calendar
from datetime import datetime, timedelta

from flask import current_app
from jwt import DecodeError

from project.dao import AuthDAO
from project.dao.models import User
from project.services.base import BaseService
from project.schemas.auth import AuthUserSchema

from project.tools.security import generate_password_digest, generate_password_b64
from project.exceptions import UserNotFound, WrongPassword, InvalidTokens

user_created_schema = AuthUserSchema()


class AuthService(BaseService[AuthDAO]):
    def __get_hash(self, password: str) -> str:
        password_hash_digest = generate_password_digest(password)
        password_hash_b64 = generate_password_b64(password_hash_digest)

        return password_hash_b64.decode('utf-8')

    def __compare_password_digest(self, password1, password2) -> bool:
        return hmac.compare_digest(password1, password2)

    def __generate_tokens(self, user: User):

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

        return tokens

    def register(self, password: str, email: str) -> AuthUserSchema:
        password_hash = self.__get_hash(password)
        new_user = self.dao.create(email=email, password_hash=password_hash)

        return user_created_schema.dump(new_user)

    def login(self, password: str, email: str) -> dict:
        user = self.dao.get_user_by_email(email=email)
        if user is None:
            raise UserNotFound

        password_hash = self.__get_hash(password)

        if not self.__compare_password_digest(password1=password_hash, password2=user.password_hash):
            raise WrongPassword

        return self.__generate_tokens(user)

    def approve_tokens(self, tokens: dict[str, str]):
        try:
            access_token_data = jwt.decode(
                jwt=tokens['access_token'],
                key=current_app.config['SECRET_KEY'],
                algorithms=current_app.config['JWT_ALGO']
            )
            refresh_token_data = jwt.decode(
                jwt=tokens['refresh_token'],
                key=current_app.config['SECRET_KEY'],
                algorithms=current_app.config['JWT_ALGO']
            )
        except DecodeError:
            raise InvalidTokens

        user = self.dao.get_user_by_email(email=refresh_token_data['email'])
        if user is None:
            raise UserNotFound
        return self.__generate_tokens(user)

    def update_password(self, email, password1, password2):
        user = self.dao.get_user_by_email(email=email)
        if user is None:
            raise UserNotFound

        old_password_hash = self.__get_hash(password1)

        if not self.__compare_password_digest(password1=old_password_hash, password2=user.password_hash):
            raise WrongPassword

        new_password_hash = self.__get_hash(password2)

        self.dao.update_user_password(email=email, new_password_hash=new_password_hash)
