from dataclasses import dataclass, field


@dataclass(frozen=True)
class PostgresConfig:
    host: str = field(default="localhost")
    port: int = field(default=5432)
    user: str = field(default="postgres")
    password: str = field(default="postgres")
    database: str = field(default="postgres")
    echo: bool = field(default=True)

    @property
    def postgres_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
