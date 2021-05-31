class Error(Exception):
    """Base class for other exceptions"""

    def __init__(self, message="The request could not be processed."):
        self.message = message
        super().__init__(self.message)


class MatchNotFoundError(Error):
    message = "The match was not found."


class MatchRequestNotFoundError(Error):
    message = "The match request was not found."


class MatchTermNotFoundError(Error):
    message = "The term was not found."


class JWTError(Error):
    pass
