
from .constants import *

class BaseHttpException(Exception):

    def __init__(self, code: int, message):

        self.code = code

        self.message = message


class UnauthorizedError(BaseHttpException):
    def __init__(self, message: str = ''):
        super().__init__(UNAUTHORIZED, message)

class ForbiddenError(BaseHttpException):
    def __init__(self, message: str = ''):
        super().__init__(FORBIDDEN, message)

class MethodNotAllowedError(BaseHttpException):
    def __init__(self, message: str = ''):
        super().__init__(METHOD_NOT_ALLOWED, message)

class BadRequestError(BaseHttpException):
    def __init__(self, message: str):
        super().__init__(BAD_REQUEST, message)

class NotFoundError(BaseHttpException):
    def __init__(self, message: str):
        super().__init__(NOT_FOUND, message)
