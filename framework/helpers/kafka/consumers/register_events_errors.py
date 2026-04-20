import time

from framework.internal.kafka.subscriber import Subscriber
from framework.settings import settings


class RegisterEventsErrorsSubscribers(Subscriber):
    topic: str = settings.topic_register_events_errors

    def find_message(self, login: str, error_type: str | None = None, timeout: float = 10.0):
        start_time = time.time()

        while time.time() - start_time < timeout:
            message = self.get_message(timeout=timeout)
            msg_login = message.value["input_data"]["login"]
            msg_error_type = message.value["error_type"]

            if msg_login == login:
                if error_type is None or msg_error_type == error_type:
                    return message
        raise AssertionError(
            f"Message with login '{login}' and error_type '{error_type}' not found after {timeout} s")
