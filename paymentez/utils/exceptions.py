from typing import Optional
from enum import Enum


class PaymentezException(Exception):
    code: int
    message: str
    type: Optional[str]
    description: Optional[str]

    def __init__(self, code, message, type, description) -> None:
        self.code = code
        self.message = message
        self.type = type
        self.description = description

        super().__init__(message)


class PaymentezErrorCode(Enum):
    MISSING_KEYS = 1
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    SERVER_ERROR = 500
    SERVICE_UNAVAILABLE = 503
