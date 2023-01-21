class TonapiException(Exception):
    def __init__(self, error: str | dict):
        if isinstance(error, dict):
            error = error.get("error")
        super().__init__(error)


class TonapiError(TonapiException):
    ...


class TonapiUnauthorized(TonapiException):
    ...
