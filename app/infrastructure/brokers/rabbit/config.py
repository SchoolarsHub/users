from dataclasses import dataclass, field


@dataclass(frozen=True)
class RabbitConfig:
    host: str = field(default="localhost")
    port: int = field(default=5672)
    username: str = field(default="guest")
    password: str = field(default="guest")
    queue: str = field(default="users")
    exchange: str = field(default="users")

    @property
    def rabbit_url(self) -> str:
        return f"amqp://{self.username}:{self.password}@{self.host}:{self.port}/"
