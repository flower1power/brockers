from abc import ABC, abstractmethod
from typing import Any

from kafka.producer.future import RecordMetadata

from framework.internal.kafka.producer import Producer


class Publisher(ABC):
    def __init__(self, producer: Producer):
        self._producer = producer

    @property
    @abstractmethod
    def topic(self) -> str:
        ...

    def send(self, msg: dict[Any, Any]) -> RecordMetadata:
        return self._producer.send(topic=self.topic, msg=msg)
