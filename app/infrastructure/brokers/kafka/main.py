from faststream.kafka import KafkaBroker as Broker
from faststream.kafka.annotations import KafkaBroker
from faststream.security import SASLPlaintext

from app.infrastructure.brokers.kafka.config import KafkaConfig


def setup_kafka_broker(config: KafkaConfig, security: SASLPlaintext) -> KafkaBroker:
    return Broker(bootstrap_servers=config.kafka_url, security=security)
