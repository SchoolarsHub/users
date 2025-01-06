from dataclasses import dataclass, field
from tomllib import load

from adaptix import Retort

from app.infrastructure.brokers.rabbit.config import RabbitConfig
from app.infrastructure.databases.postgres.config import PostgresConfig

CONFIG_PATH = "./conf/app_config.toml"


@dataclass(frozen=True)
class Config:
    rabbit: RabbitConfig = field(default_factory=RabbitConfig)
    postgres: PostgresConfig = field(default_factory=PostgresConfig)

    @staticmethod
    def load_variables() -> "Config":
        with open(CONFIG_PATH, "rb") as f:
            config = load(f)

        retort = Retort()

        return retort.load(config, Config)
