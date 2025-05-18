GENERIC_EXCEPTION_MESSAGE = "Generic Exception"
GENERIC_EXCEPTION_CODE = 500


class CustomException(Exception):
    def __init__(
        self, msg: str = GENERIC_EXCEPTION_MESSAGE, code: int = GENERIC_EXCEPTION_CODE
    ):
        self.msg = msg
        self.code = code


class InvalidParameters(CustomException):
    msg = "Invalid Params"
    code = 400


class NotImplemented(CustomException):
    msg = "Not implemented yet"
    code = 501
