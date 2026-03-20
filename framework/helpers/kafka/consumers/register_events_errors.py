from framework.internal.kafka.subscriber import Subscriber
from framework.settings.settings import TOPIC_REGISTER_EVENTS_ERRORS


class RegisterEventsErrorsSubscribers(Subscriber):
    topic: str = TOPIC_REGISTER_EVENTS_ERRORS

    def find_message(self, login: str, error_type: str | None = None):
        for i in range(10):
            message = self.get_message()
            msg_login = message.value["input_data"]["login"]
            msg_error_type = message.value["error_type"]

            if msg_login == login:
                if error_type is None or msg_error_type == error_type:
                    return message
        raise AssertionError(f"Message with login '{login}' and error_type '{error_type}' not found after 10 attempts")
