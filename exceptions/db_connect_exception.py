from .connect_exception import ConnectException


class DatabaseConnectException(ConnectException):
    def __init__(self, message: str = ''):
        super().__init__(message=message)