from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection

from app.domain.model.linked_account.linked_account import LinkedAccount
from app.infrastructure.databases.postgres.gateways.generic_datamapper import GenericDataMapper


class LinkedAccountDataMapper(GenericDataMapper[LinkedAccount]):
    def __init__(self, connection: AsyncConnection) -> None:
        self.connection = connection

    async def save(self, entity: LinkedAccount) -> None:
        stmt = text(
            """
            INSERT INTO linked_accounts (linked_account_id, user_id, social_network, connection_link, connected_at, connection_reason)
            VALUES (:linked_account_id, :user_id, :social_network, :cconnection_link, :connected_at, connection_reason)
            """
        ).bindparams(
            entity.linked_account_id, entity.user_id, entity.social_network, entity.connection_link, entity.connected_at, entity.connected_for
        )

        await self.connection.execute(stmt)

    async def update(self, entity: LinkedAccount) -> None:
        stmt = text(
            """
            UPDATE linked_accounts
            SET (linked_account_id, user_id, social_network, connection_link, connected_at, connection_reason)
            VALUES (:linked_account_id, :user_id, :social_network, :cconnection_link, :connected_at, connection_reason)
            WHERE linked_account_id = :linked_account_id
            """
        ).bindparams(
            entity.linked_account_id, entity.user_id, entity.social_network, entity.connection_link, entity.connected_at, entity.connected_for
        )

        await self.connection.execute(stmt)

    async def delete(self, entity: LinkedAccount) -> None:
        stmt = text(
            """
            DELETE FROM linked_accounts WHERE linked_account_id = :linked_account_id
            """
        ).bindparams(entity.linked_account_id)

        await self.connection.execute(stmt)
