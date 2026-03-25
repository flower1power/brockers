from abc import ABC, abstractmethod

import pika

from framework.internal.rmq.publisher import RmqPublisher


class BasePublisher(ABC):
    def __init__(self, publisher: RmqPublisher):
        self._publisher = publisher

    @property
    @abstractmethod
    def exchange(self) -> str:
        ...

    @property
    @abstractmethod
    def routing_key(self) -> str:
        ...

    def publish(
            self,
            message: dict[str, str],
            properties: pika.BasicProperties | None = None
    ):
        return self._publisher.publish(
            exchange=self.exchange,
            message=message,
            routing_key=self.routing_key,
            properties=properties
        )
