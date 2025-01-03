from dataclasses import dataclass, field


@dataclass(frozen=True)
class KafkaConfig:
    host: str = field(default="localhost")
    port: int = field(default=9092)
    topic: str = field(default="users")
    username: str = field(default="admin")
    password: str = field(default="admin")

    @property
    def kafka_url(self) -> str:
        return f"{self.host}:{self.port}"
