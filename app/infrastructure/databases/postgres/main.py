from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, create_async_engine

from app.infrastructure.databases.postgres.config import PostgresConfig


async def setup_sqla_engine(config: PostgresConfig) -> AsyncEngine:
    sqla_engine = create_async_engine(
        url=config.postgres_url,
        echo=config.echo,
    )

    return sqla_engine


async def setup_sqla_connection(engine: AsyncEngine) -> AsyncGenerator[AsyncConnection, None]:
    async with engine.begin() as connection:
        yield connection
