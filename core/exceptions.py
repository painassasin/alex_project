class BaseAppException(Exception):
    message: str = 'Something went wrong'

    def __init__(self, *args):
        if args and args[0]:
            self.message = str(args[0])

    def __str__(self):
        return self.message


class BadRequest(BaseAppException):
    pass


class ParseError(BaseAppException):
    pass
