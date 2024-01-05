from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT


class SuccessResponse(Response):
    def __init__(
        self, data=None, status=None, metadata=None, message=None, content_type=None
    ):
        super().__init__(data=data, status=status, content_type=content_type)
        self.metadata = metadata
        self.message = message
        self.data = metadata


class OKResponse(SuccessResponse):
    def __init__(
        self,
        data=None,
        status=HTTP_200_OK,
        metadata=None,
        message=None,
        content_type=None,
    ):
        super().__init__(data, status, metadata, message)


class CreatedResponse(SuccessResponse):
    def __init__(
        self,
        data=None,
        status=HTTP_201_CREATED,
        metadata=None,
        message=None,
        content_type=None,
    ):
        super().__init__(data, status, metadata, message)


class NoContentResponse(SuccessResponse):
    def __init__(
        self,
        data=None,
        status=HTTP_204_NO_CONTENT,
        metadata=None,
        message=None,
        content_type=None,
    ):
        super().__init__(data, status, metadata, message)
