from dataclasses import dataclass, field

from app.infrastructure.brokers.kafka.config import KafkaConfig
from app.infrastructure.databases.postgres.config import PostgresConfig


@dataclass(frozen=True)
class Config:
    kafka: KafkaConfig = field(default_factory=KafkaConfig)
    postgres: PostgresConfig = field(default_factory=PostgresConfig)
