from faststream.kafka import KafkaBroker as Broker
from faststream.kafka.annotations import KafkaBroker
from faststream.security import SASLPlaintext

from app.infrastructure.brokers.kafka.config import KafkaConfig


async def setup_kafka_broker(config: KafkaConfig, security: SASLPlaintext) -> KafkaBroker:
    broker = Broker(bootstrap_servers=config.kafka_url)
    await broker.start()
    return broker
