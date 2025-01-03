from sqlalchemy import delete, insert, update
from sqlalchemy.ext.asyncio import AsyncConnection

from app.domain.model.linked_account.linked_account import LinkedAccount
from app.infrastructure.databases.postgres.gateways.generic_datamapper import GenericDataMapper


class LinkedAccountDataMapper(GenericDataMapper[LinkedAccount]):
    def __init__(self, connection: AsyncConnection) -> None:
        self.connection = connection

    async def save(self, entity: LinkedAccount) -> None:
        stmt = insert(LinkedAccount).values(
            linked_account_id=entity.linked_account_id,
            user_id=entity.user_id,
            social_network=entity.social_network,
            connection_link=entity.connection_link,
            connected_at=entity.connected_at,
            connection_reason=entity.connected_for,
        )

        await self.connection.execute(stmt)

    async def update(self, entity: LinkedAccount) -> None:
        stmt = (
            update(LinkedAccount)
            .where(LinkedAccount.linked_account_id == entity.linked_account_id)
            .values(
                social_network=entity.social_network,
                connection_link=entity.connection_link,
                connected_at=entity.connected_at,
                connection_reason=entity.connected_for,
            )
        )

        await self.connection.execute(stmt)

    async def delete(self, entity: LinkedAccount) -> None:
        stmt = delete(LinkedAccount).where(LinkedAccount.linked_account_id == entity.linked_account_id)

        await self.connection.execute(stmt)