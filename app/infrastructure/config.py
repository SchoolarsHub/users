from dataclasses import dataclass, field

from app.infrastructure.brokers.rabbit.config import RabbitConfig
from app.infrastructure.databases.postgres.config import PostgresConfig


@dataclass(frozen=True)
class Config:
    rabbit: RabbitConfig = field(default_factory=RabbitConfig)
    postgres: PostgresConfig = field(default_factory=PostgresConfig)
