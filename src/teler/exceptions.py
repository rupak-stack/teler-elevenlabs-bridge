GENERIC_EXCEPTION_MESSAGE = "Generic Exception"
GENERIC_EXCEPTION_CODE = 500


class TelerException(Exception):
    def __init__(
        self, msg: str = GENERIC_EXCEPTION_MESSAGE, code: int = GENERIC_EXCEPTION_CODE
    ):
        self.msg = msg
        self.code = code


class InvalidParameters(TelerException):
    msg = "Invalid Parameters"
    code = 400


class NotImplemented(TelerException):
    msg = "Not implemented"
    code = 501


class InvalidStreamOperation(TelerException):
    msg = "Invalid Stream Operation"
    code = 400
