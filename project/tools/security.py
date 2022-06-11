import hashlib
import base64

from flask import current_app


def generate_password_digest(password) -> bytes:
    return hashlib.pbkdf2_hmac(
        hash_name=current_app.config["PWD_HASH_ALGO"],
        password=password.encode("utf-8"),
        salt=current_app.config["PWD_HASH_SALT"],
        iterations=current_app.config["PWD_HASH_ITERATIONS"]
    )


def generate_password_b64(password_digest: bytes) -> bytes:
    return base64.b64encode(password_digest)
