import uuid
from typing import Callable, Generator

import pytest

from framework.helpers.account_helper import AccountHelper
from framework.helpers.kafka.consumers.register_events import RegisterEventsSubscribers
from framework.helpers.kafka.consumers.register_events_errors import RegisterEventsErrorsSubscribers
from framework.helpers.kafka.publishers.register_events import RegisterEventsPublisher
from framework.helpers.kafka.publishers.register_events_errors import RegisterEventsErrorsPublisher
from framework.helpers.rmq.consumers.dm_mail_sending import DmMailSendingConsumer
from framework.helpers.rmq.publishers.dm_mail_sending import DmMailSendingPublisher
from framework.internal.http.account.account import AccountApi
from framework.internal.http.mail.mail import MailApi
from framework.internal.http.models.ErrorMessage import ErrorMessage
from framework.internal.http.models.RmqMessageMailBody import RmqMessageMailBody
from framework.internal.http.models.UserPayload import UserPayload
from framework.internal.kafka.consumer import Consumer
from framework.internal.kafka.producer import Producer
from framework.internal.rmq.publisher import RmqPublisher
from framework.settings import settings


@pytest.fixture(scope="session")
def account() -> AccountApi:
    return AccountApi(base_url=settings.base_url_api)


@pytest.fixture(scope="session")
def mail() -> MailApi:
    return MailApi(base_url=settings.base_url_api)


@pytest.fixture
def account_helper(account: AccountApi, mail: MailApi) -> AccountHelper:
    return AccountHelper(account, mail)


@pytest.fixture(scope="session")
def kafka_producer() -> Generator[Producer, None, None]:
    with Producer([settings.kafka_producer]) as producer:
        yield producer


@pytest.fixture(scope="session")
def rmq_publisher() -> Generator[RmqPublisher, None, None]:
    with RmqPublisher(settings.rmq_publisher_url) as rmq_publisher:
        yield rmq_publisher


@pytest.fixture(scope="session")
def dm_mail_sending_publisher(rmq_publisher: RmqPublisher) -> DmMailSendingPublisher:
    return DmMailSendingPublisher(rmq_publisher)


@pytest.fixture(scope="session")
def register_events_subscriber() -> RegisterEventsSubscribers:
    return RegisterEventsSubscribers()


@pytest.fixture(scope="session")
def register_events_error_subscriber() -> RegisterEventsErrorsSubscribers:
    return RegisterEventsErrorsSubscribers()


@pytest.fixture(scope="session")
def register_events_publisher(kafka_producer: Producer) -> RegisterEventsPublisher:
    return RegisterEventsPublisher(kafka_producer)


@pytest.fixture(scope="session")
def register_events_errors_publisher(kafka_producer: Producer) -> RegisterEventsErrorsPublisher:
    return RegisterEventsErrorsPublisher(kafka_producer)


@pytest.fixture(scope="session", autouse=True)
def kafka_consumer(
        register_events_subscriber: RegisterEventsSubscribers,
        register_events_error_subscriber: RegisterEventsErrorsSubscribers
) -> Generator[Consumer, None, None]:
    with Consumer(
            subscribers=[register_events_subscriber, register_events_error_subscriber],
            bootstrap_servers=[settings.kafka_producer]
    ) as consumer:
        yield consumer


@pytest.fixture(scope="session", autouse=True)
def rmq_mail_sending_consumer() -> Generator[DmMailSendingConsumer, None, None]:
    with DmMailSendingConsumer(settings.rmq_publisher_url) as consumer:
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
def prepare_rmq_message_mail() -> RmqMessageMailBody:
    address = f"{uuid.uuid4().hex}@mail.ru"
    return {
        "address": address,
        "subject": "New message test",
        "body": "New body test",
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
def prepare_error_validation(
        prepare_user: UserPayload,
        error_message_factory
) -> ErrorMessage:
    return error_message_factory(prepare_user, "unknown")


@pytest.fixture
def prepare_error_msg_register_events_error(error_message_factory) -> ErrorMessage:
    user: UserPayload = {
        "login": "string1",
        "email": "string1@mail.ru",
        "password": "string1"
    }
    return error_message_factory(user, "unknown")
