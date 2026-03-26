from typing import TypedDict


class UserPayload(TypedDict):
    login: str
    email: str
    password: str
