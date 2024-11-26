from fastapi import HTTPException, status


class CustomHTTPException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail: str = "",
        error_type: str = "CustomHTTPException",
    ):
        super().__init__(status_code=status_code, detail=detail)
        self.error_type = error_type


class ServerHTTPException(CustomHTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail: str = "",
        error_type: str = "ServerHTTPException",
    ):
        super().__init__(
            status_code=status_code, detail=detail, error_type=error_type
        )


class ClientHTTPException(CustomHTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: str = "",
        error_type: str = "ClientHTTPException",
    ):
        super().__init__(
            status_code=status_code, detail=detail, error_type=error_type
        )


class DatabaseException(Exception):
    def __init__(self, message: str, extra_info: str = ""):
        super().__init__(message)
        self.extra_info = extra_info
