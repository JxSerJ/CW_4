class BaseError(Exception):
    pass


class ItemNotFound(BaseError):
    pass


class UserNotFound(BaseError):
    pass


class IncorrectPassword(BaseError):
    pass


class InvalidTokens(BaseError):
    pass
