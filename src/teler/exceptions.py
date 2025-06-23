class TelerException(Exception):
    message = "An exception occurred."
    code = 500

    def __init__(self, msg: str = message):
        super().__init__(msg)


class UnauthorizedException(Exception):
    message = "Unauthorized"
    code = 401


class ForbiddenException(Exception):
    message = "Forbidden"
    code = 403


class BadParametersException(TelerException):
    message = "Bad Parameter(s)"
    code = 400

    def __init__(self, param: str = "", msg: str = message):
        self.param = param
        super().__init__(msg)


class NotImplementedException(TelerException):
    message = "Not implemented"
    code = 501

    def __init__(self, msg: str = message):
        super().__init__(msg)
