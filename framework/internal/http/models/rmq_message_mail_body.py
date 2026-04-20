from typing import TypedDict


class RmqMessageMailBody(TypedDict):
    address: str
    subject: str
    body: str
