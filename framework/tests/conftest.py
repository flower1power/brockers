import uuid

import pytest

from framework.helpers.account_helper import AccountHelper
from framework.internal.http.account.account import AccountApi
from framework.internal.http.mail.mail import MailApi
from framework.internal.http.models.ErrorMessage import ErrorMessage
from framework.internal.http.models.UserPayload import UserPayload
from framework.internal.kafka.producer import Producer
from framework.settings.settings import BASE_URL_API


@pytest.fixture(scope="session")
def account() -> AccountApi:
    return AccountApi(base_url=BASE_URL_API)


@pytest.fixture(scope="session")
def mail() -> MailApi:
    return MailApi(base_url=BASE_URL_API)


@pytest.fixture(scope="session")
def kafka_producer() -> Producer:
    with Producer() as producer:
        yield producer


@pytest.fixture()
def account_helper(account: AccountApi, mail: MailApi):
    account_helper = AccountHelper(account, mail)
    return account_helper


@pytest.fixture
def prepare_user() -> UserPayload:
    base = uuid.uuid4().hex
    return {
        "login": base,
        "email": f"{base}@mail.ru",
        "password": "123123123",
    }


@pytest.fixture
def prepare_error_validation(prepare_user) -> ErrorMessage:
    user_data = prepare_user
    return {
        "input_data": {
            "login": user_data["login"],
            "email": user_data["email"],
            "password": user_data["password"]
        },
        "error_message": {
            "type": "https://tools.ietf.org/html/rfc7231#section-6.5.1",
            "title": "Validation failed",
            "status": 400,
            "traceId": "00-2bd2ede7c3e4dcf40c4b7a62ac23f448-839ff284720ea656-01",
            "errors": {
                "Email": [
                    "Invalid"
                ]
            }
        },
        "error_type": "unknown"
    }
