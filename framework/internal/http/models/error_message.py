from typing import TypedDict

from framework.internal.http.models.user_payload import UserPayload


class ErrorMessageBody(TypedDict):
    type: str
    title: str
    status: int
    traceId: str
    errors: dict[str, list[str]]


class ErrorMessage(TypedDict):
    input_data: UserPayload
    error_message: ErrorMessageBody
    error_type: str
