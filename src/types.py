class Undefined:
    pass


class ValidationError(Exception):
    def __init__(self, msg: str):
        self.msg = msg
