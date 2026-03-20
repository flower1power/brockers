import uuid
from typing import Callable, Generator

import pytest

from framework.helpers.account_helper import AccountHelper
from framework.helpers.kafka.consumers.register_events import RegisterEventsSubscribers
from framework.helpers.kafka.consumers.register_events_errors import RegisterEventsErrorsSubscribers
from framework.internal.http.account.account import AccountApi
from framework.internal.http.mail.mail import MailApi
from framework.internal.http.models.ErrorMessage import ErrorMessage
from framework.internal.http.models.UserPayload import UserPayload
from framework.internal.kafka.consumer import Consumer
from framework.internal.kafka.producer import Producer
from framework.settings.settings import BASE_URL_API


@pytest.fixture(scope="session")
def account() -> AccountApi:
    return AccountApi(base_url=BASE_URL_API)


@pytest.fixture(scope="session")
def mail() -> MailApi:
    return MailApi(base_url=BASE_URL_API)


@pytest.fixture
def account_helper(account: AccountApi, mail: MailApi) -> AccountHelper:
    return AccountHelper(account, mail)


@pytest.fixture(scope="session")
def kafka_producer() -> Generator[Producer, None, None]:
    with Producer() as producer:
        yield producer


@pytest.fixture(scope="session")
def register_events_subscriber() -> RegisterEventsSubscribers:
    return RegisterEventsSubscribers()


@pytest.fixture(scope="session")
def register_events_error_subscriber() -> RegisterEventsErrorsSubscribers:
    return RegisterEventsErrorsSubscribers()


@pytest.fixture(scope="session", autouse=True)
def kafka_consumer(
        register_events_subscriber: RegisterEventsSubscribers,
        register_events_error_subscriber: RegisterEventsErrorsSubscribers
) -> Generator[Consumer, None, None]:
    with Consumer(subscribers=[register_events_subscriber, register_events_error_subscriber]) as consumer:
        yield consumer


@pytest.fixture
def prepare_user() -> UserPayload:
    base = uuid.uuid4().hex
    return {
        "login": base,
        "email": f"{base}@mail.ru",
        "password": "123123123",
    }


@pytest.fixture
def error_message_factory() -> Callable[[UserPayload, str], ErrorMessage]:
    def _create(user: UserPayload, error_type: str = "unknown") -> ErrorMessage:
        return {
            "input_data": user,
            "error_message": {
                "type": "https://tools.ietf.org/html/rfc7231#section-6.5.1",
                "title": "Validation failed",
                "status": 400,
                "traceId": f"00-{uuid.uuid4().hex}-01",
                "errors": {"Email": ["Invalid"]}
            },
            "error_type": error_type
        }

    return _create


@pytest.fixture
def prepare_error_validation(prepare_user: UserPayload, error_message_factory) -> ErrorMessage:
    return error_message_factory(prepare_user, "unknown")


@pytest.fixture
def prepare_error_msg_register_events_error(error_message_factory) -> ErrorMessage:
    user: UserPayload = {
        "login": "string1",
        "email": "string1@mail.ru",
        "password": "string1"
    }
    return error_message_factory(user, "unknown")
