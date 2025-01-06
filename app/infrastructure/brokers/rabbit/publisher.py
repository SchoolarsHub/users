from faststream.rabbit.annotations import RabbitBroker

from app.infrastructure.brokers.message import Message
from app.infrastructure.brokers.publisher import MessagePublisher
from app.infrastructure.brokers.rabbit.config import RabbitConfig


class MessagePublisherImpl(MessagePublisher):
    def __init__(self, broker: RabbitBroker, config: RabbitConfig) -> None:
        self.broker = broker
        self.config = config

    async def publish(self, message: Message) -> None:
        await self.broker.publish(message=message.as_dict(), queue=self.config.queue)
