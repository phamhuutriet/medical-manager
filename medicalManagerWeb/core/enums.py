from enum import Enum


class GENDER(Enum):
    M = "M"
    F = "F"
    O = "O"


class TemplateColumnType(Enum):
    TEXT = "TEXT"
    IMAGE = "IMAGE"


class Header(Enum):
    CLIENT_ID = "X-Client-ID"
    AUTHORIZATION = "local-authorization"