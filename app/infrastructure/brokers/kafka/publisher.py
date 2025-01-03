from faststream.kafka.annotations import KafkaBroker

from app.infrastructure.brokers.kafka.config import KafkaConfig
from app.infrastructure.brokers.message import Message
from app.infrastructure.brokers.publisher import MessagePublisher


class MessagePublisherImpl(MessagePublisher):
    def __init__(self, broker: KafkaBroker, config: KafkaConfig) -> None:
        self.broker = broker
        self.config = config

    async def publish(self, message: Message) -> None:
        await self.broker.publish(message=message.as_dict(), topic=self.config.topic)
