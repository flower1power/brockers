from framework.internal.kafka.producer import Producer
from framework.tests.conftest import account_helper


def test_failed_registration(account_helper) -> None:
    account_helper.failed_register_user(login="string", email="string@mail.ru", password="string")


def test_success_registration(prepare_user, account_helper) -> None:
    user = prepare_user
    account_helper.success_register_user(login=user["login"], email=user["email"], password=user["password"])


def test_success_registration_with_kafka(kafka_producer: Producer, prepare_user, account_helper) -> None:
    msg = prepare_user
    kafka_producer.send(topic="register-events", msg=msg)
    account_helper.find_msg(msg["login"])


def test_register_events_error_consumer(
        kafka_producer: Producer,
        prepare_error_validation,
        account_helper
) -> None:
    msg = prepare_error_validation
    kafka_producer.send(topic="register-events-errors", msg=msg)
    account_helper.find_msg(msg["input_data"]["login"])
    token = account_helper.get_activation_token_by_login(msg["input_data"]["login"])
    account_helper.account_api.activate_user(token)
