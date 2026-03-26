from framework.internal.rmq.base_publisher import BasePublisher
from framework.settings import settings


class DmMailSendingPublisher(BasePublisher):
    exchange = settings.dm_mail_sending_exchange
    routing_key = ""
