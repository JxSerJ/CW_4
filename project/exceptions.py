class BaseError(Exception):
    pass


class ItemNotFound(BaseError):
    pass


class UserNotFound(BaseError):
    pass


class WrongPassword(BaseError):
    pass


class InvalidTokens(BaseError):
    pass
