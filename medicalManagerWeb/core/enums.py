from enum import Enum


class GENDER(Enum):
    M = "M"
    F = "F"
    O = "O"


class TemplateColumnType(Enum):
    TEXT = "TEXT"
    IMAGE = "IMAGE"


class Header(Enum):
    CLIENT_ID = "x-client-id"
    AUTHORIZATION = "authorization"