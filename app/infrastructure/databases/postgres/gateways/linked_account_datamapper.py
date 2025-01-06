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
            VALUES (:linked_account_id, :user_id, :social_network, :connection_link, :connected_at, :connection_reason)
            """
        ).bindparams(
            linked_account_id=entity.linked_account_id,
            user_id=entity.user_id,
            social_network=entity.social_network,
            connection_link=entity.connection_link,
            connected_at=entity.connected_at,
            connection_reason=entity.connected_for,
        )

        await self.connection.execute(stmt)

    async def update(self, entity: LinkedAccount) -> None:
        stmt = text(
            """
            UPDATE linked_accounts
            SET social_network = :social_network,
                connection_link = :connection_link,
                connected_at = :connected_at,
                connection_reason = :connection_reason
            WHERE linked_account_id = :linked_account_id
            """
        ).bindparams(
            linked_account_id=entity.linked_account_id,
            social_network=entity.social_network,
            connection_link=entity.connection_link,
            connected_at=entity.connected_at,
            connection_reason=entity.connected_for,
        )

        await self.connection.execute(stmt)

    async def delete(self, entity: LinkedAccount) -> None:
        stmt = text(
            """
            DELETE FROM linked_accounts WHERE linked_account_id = :linked_account_id
            """
        ).bindparams(linked_account_id=entity.linked_account_id)

        await self.connection.execute(stmt)
