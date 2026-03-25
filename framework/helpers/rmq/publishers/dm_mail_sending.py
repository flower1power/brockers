from framework.internal.rmq.base_publisher import BasePublisher
from framework.settings import settings


class DmMailSendingPublisher(BasePublisher):
    @property
    def exchange(self) -> str:
        return settings.dm_mail_sending_exchange

    @property
    def routing_key(self) -> str:
        return ""
