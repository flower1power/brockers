from framework.internal.kafka.subscriber import Subscriber
from framework.settings import settings


class RegisterEventsSubscribers(Subscriber):
    topic: str = settings.topic_register_events

    def find_message(self, login: str):
        for i in range(10):
            message = self.get_message()
            if message.value["login"] == login:
                return message
        raise AssertionError(f"Message with login '{login}' not found after 10 attempts")
