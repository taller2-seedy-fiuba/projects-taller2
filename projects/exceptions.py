"""Custom exceptions."""


class ParamDoesNotAllowedException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class ProjectNotFound(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
