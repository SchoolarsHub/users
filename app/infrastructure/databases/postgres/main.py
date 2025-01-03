from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, create_async_engine

from app.domain.model.linked_account.linked_account import LinkedAccount
from app.domain.model.user.user import User
from app.infrastructure.databases.postgres.config import PostgresConfig
from app.infrastructure.databases.postgres.gateways.linked_account_datamapper import GenericDataMapper
from app.infrastructure.databases.postgres.registry import Registry


async def setup_sqla_engine(config: PostgresConfig) -> AsyncEngine:
    sqla_engine = create_async_engine(
        url=config.postgres_url,
        echo=config.echo,
    )

    return sqla_engine


async def setup_sqla_connection(engine: AsyncEngine) -> AsyncGenerator[AsyncConnection, None]:
    async with engine.begin() as connection:
        yield connection


def setup_datamappers(registry: Registry) -> None:
    registry.add_mapper(User, GenericDataMapper[User])
    registry.add_mapper(LinkedAccount, GenericDataMapper[LinkedAccount])
