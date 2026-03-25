import json
import time

from framework.internal.rmq.consumer import Consumer
from framework.settings import settings


class DmMailSendingConsumer(Consumer):
    exchange = settings.dm_mail_sending_exchange
    routing_key = "#"

    def find_message(self, login: str, timeout: float = 10.0):
        start_time = time.time()

        while time.time() - start_time < timeout:
            message = self.get_message(timeout=timeout)
            if json.loads(message["body"])["Login"] == login:
                return message

        else:
            raise AssertionError(f"Message with login '{login}' not found after {timeout} s")
