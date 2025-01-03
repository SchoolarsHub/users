import ssl
from ssl import SSLContext

from faststream.security import SASLPlaintext

from app.infrastructure.brokers.kafka.config import KafkaConfig


def setup_ssl_context() -> SSLContext:
    return ssl.create_default_context()


def setup_kafka_security(ssl_context: SSLContext, kafka_config: KafkaConfig) -> SASLPlaintext:
    return SASLPlaintext(
        ssl_context=ssl_context,
        username=kafka_config.username,
        password=kafka_config.password,
    )
