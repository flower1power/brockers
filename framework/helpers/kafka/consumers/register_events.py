from framework.internal.kafka.subscriber import Subscriber
from framework.settings.settings import TOPIC_REGISTER_EVENTS


class RegisterEventsSubscribers(Subscriber):
    topic: str = TOPIC_REGISTER_EVENTS

    def find_message(self, login: str):
        for i in range(10):
            message = self.get_message()
            if message.value["login"] == login:
                return message
        raise AssertionError(f"Message with login '{login}' not found after 10 attempts")
