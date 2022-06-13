import hashlib
import base64

import jwt
from flask import current_app, request
from flask_restx import abort
from jwt import DecodeError, ExpiredSignatureError


def generate_password_digest(password) -> bytes:
    return hashlib.pbkdf2_hmac(
        hash_name=current_app.config["PWD_HASH_ALGO"],
        password=password.encode("utf-8"),
        salt=current_app.config["PWD_HASH_SALT"].encode("utf-8"),
        iterations=current_app.config["PWD_HASH_ITERATIONS"]
    )


def generate_password_b64(password_digest: bytes) -> bytes:
    return base64.b64encode(password_digest)


def decode_jwt(token) -> dict[str, any]:
    """Decodes jwt and returns jwt-payload"""
    token_data = jwt.decode(
        jwt=token,
        key=current_app.config['SECRET_KEY'],
        algorithms=current_app.config['JWT_ALGO']
    )
    return token_data


def auth_required(func):
    def wrapper(*args, **kwargs):
        if "Authorization" not in request.headers:
            abort(401, "Authorization required")

        token = request.headers["Authorization"].split("Bearer ")[-1]

        try:
            decode_jwt(token)
        except DecodeError:
            abort(400, message="Invalid token")
        except ExpiredSignatureError:
            abort(401, message="Signature has expired")

        email = decode_jwt(token)['email']

        return func(email, **kwargs)

    return wrapper
