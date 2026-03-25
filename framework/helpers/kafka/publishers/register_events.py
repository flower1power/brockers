from framework.internal.kafka.publisher import Publisher
from framework.settings import settings


class RegisterEventsPublisher(Publisher):
    @property
    def topic(self) -> str:
        return settings.topic_register_events
