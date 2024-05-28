from chalice import ChaliceUnhandledError


class ChaliceValidationError(ChaliceUnhandledError):

    def __init__(self, messages: dict | str, status_code: int = 422):
        self.messages = messages
        self.status_code = status_code
