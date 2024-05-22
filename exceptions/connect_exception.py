class ConnectException(Exception):
    __slots__ = ['message']

    def __init__(self,
                 message: str = ''):
        self.message = message

    def __str__(self):
        return str(self.message)