from rest_framework.response import Response
from rest_framework.status import (
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)


class ErrorResponse(Response):
    def __init__(self, data=None, status=None, metadata=None, message=None):
        super().__init__(data, status)
        self.metadata = metadata
        self.message = message
        self.data = {"message": self.message, "status": status, "metadata": metadata}


class NotFoundErrorResponse(ErrorResponse):
    def __init__(
        self, data=None, status=HTTP_404_NOT_FOUND, metadata=None, message=None
    ):
        super().__init__(data, status, metadata, message)


class BadRequestErrorResponse(ErrorResponse):
    def __init__(
        self, data=None, status=HTTP_400_BAD_REQUEST, metadata=None, message=None
    ):
        super().__init__(data, status, metadata, message)


class AuthFailureErrorResponse(ErrorResponse):
    def __init__(
        self, data=None, status=HTTP_401_UNAUTHORIZED, metadata=None, message=None
    ):
        super().__init__(data, status, metadata, message)
