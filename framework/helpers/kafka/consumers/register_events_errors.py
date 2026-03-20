from framework.internal.kafka.subscriber import Subscriber


class RegisterEventsErrorsSubscribers(Subscriber):
    topic: str = "register-events-errors"

    def find_message(self, login: str, error_type: str | None = None):
        for i in range(10):
            message = self.get_message()
            msg_login = message.value["input_data"]["login"]
            msg_error_type = message.value["error_type"]

            if msg_login == login:
                if error_type is None or msg_error_type == error_type:
                    return message
        raise AssertionError(f"Message with login '{login}' and error_type '{error_type}' not found after 10 attempts")
