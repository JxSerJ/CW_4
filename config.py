import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = "you-will-never-guess"
    JSON_AS_ASCII = False
    JSON_SORT_KEYS = False
    RESTX_JSON = {'ensure_ascii': False, 'indent': 2, 'sort_keys': False}

    ITEMS_PER_PAGE = 12

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    TOKEN_EXPIRE_MINUTES = 15
    TOKEN_EXPIRE_DAYS = 130

    JWT_ALGO = 'HS512'
    PWD_HASH_ALGO = 'sha512'
    PWD_HASH_SALT = "salt"
    PWD_HASH_ITERATIONS = 500_000


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    ENV = 'development'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = "postgresql://main_db_user:main_db_pass@pg_main_db/main_db"
    # SQLALCHEMY_BINDS = {'users': 'postgresql://users_db_user:users_db_pass@pg_users_db/users_db',
    #                     'tokens': 'postgresql://tokens_db_user:tokens_db_pass@pg_tokens_db/tokens_db',
    #                     'main': 'postgresql://main_db_user:main_db_pass@pg_main_db/main_db'}  # TODO delete this
