class ParserError(Exception):
    def __init__(self, message, *, token=None):
        super().__init__()
        self.message = message
        #: The token that caused (directly or indirectly) a parser error.
        self.token = token


class InvalidTokenError(ParserError):
    """Raised when an invalid token is encountered in the token stream."""


class UnknownDirectiveError(ParserError):
    """Raised when an unknown directive is encountered."""
