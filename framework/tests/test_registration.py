from framework.helpers.kafka.consumers.register_events import RegisterEventsSubscribers
from framework.helpers.kafka.consumers.register_events_errors import RegisterEventsErrorsSubscribers
from framework.helpers.kafka.publishers.register_events import RegisterEventsPublisher
from framework.helpers.kafka.publishers.register_events_errors import RegisterEventsErrorsPublisher
from framework.tests.conftest import account_helper


def test_failed_registration_validation_error(
        register_events_subscriber: RegisterEventsSubscribers,
        register_events_error_subscriber: RegisterEventsErrorsSubscribers,
        account_helper
) -> None:
    login = "string"
    email = "string@mail.ru"
    password = "string"

    account_helper.register_user(login=login, email=email, password=password)

    register_events_subscriber.find_message(login=login)

    error_msg = register_events_error_subscriber.find_message(login=login, error_type="validation")
    assert error_msg.value["error_type"] == "validation"


def test_success_registration(
        register_events_subscriber: RegisterEventsSubscribers,
        prepare_user,
        account_helper,
) -> None:
    user = prepare_user
    account_helper.register_user(login=user["login"], email=user["email"], password=user["password"])
    register_events_subscriber.find_message(user["login"])
    account_helper.find_msg(user["email"])


def test_success_registration_with_kafka(
    register_events_publisher: RegisterEventsPublisher, prepare_user, account_helper
) -> None:
    msg = prepare_user
    register_events_publisher.send(msg=msg)
    account_helper.find_msg(msg["login"])


def test_register_events_error_consumer(
    register_events_errors_publisher: RegisterEventsErrorsPublisher,
    prepare_error_validation,
    account_helper
) -> None:
    msg = prepare_error_validation
    register_events_errors_publisher.send(msg=msg)
    account_helper.find_msg(msg["input_data"]["login"])
    token = account_helper.get_activation_token_by_login(msg["input_data"]["login"])
    account_helper.account_api.activate_user(token)


def test_success_registration_with_kafka_producer(
    register_events_publisher: RegisterEventsPublisher, prepare_user
) -> None:
    msg = prepare_user
    register_events_publisher.send(msg=msg)


def test_success_registration_with_kafka_producer_consumer(
    register_events_subscriber: RegisterEventsSubscribers,
    prepare_user,
    register_events_publisher: RegisterEventsPublisher
) -> None:
    msg = prepare_user
    register_events_publisher.send(msg=msg)
    for i in range(20):
        message = register_events_subscriber.get_message()
        if message.value["login"] == msg["login"]:
            break
    else:
        raise AssertionError("Email not found")


def test_validation_msg_register_events_errors(
    register_events_error_subscriber: RegisterEventsErrorsSubscribers,
    register_events_errors_publisher: RegisterEventsErrorsPublisher,
    prepare_error_msg_register_events_error
) -> None:
    msg = prepare_error_msg_register_events_error
    login = msg["input_data"]["login"]
    register_events_errors_publisher.send(msg=msg)

    error_msg = register_events_error_subscriber.find_message(login=login, error_type="validation")
    assert error_msg.value["error_type"] == "validation"
