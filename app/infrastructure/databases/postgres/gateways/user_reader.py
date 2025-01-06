from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection

from app.application.common.dto.user_dto import UserDTO
from app.application.common.persistence.user_gateway import UserGateway
from app.infrastructure.databases.postgres.converters import convert_to_user_dto


class UserReader(UserGateway):
    def __init__(self, connection: AsyncConnection) -> None:
        self.connection = connection

    async def with_id(self, user_id: UUID) -> UserDTO | None:
        query = text(
            """
            SELECT
                u.user_id AS user_id,
                u.firstname AS firstname,
                u.lastname AS lastname,
                u.middlename AS middlename,
                u.email AS email,
                u.phone AS phone,
                u.status AS status,
                u.created_at AS created_at,
                u.deleted_at AS deleted_at,
                la.linked_account_id AS linked_account_id,
                la.user_id AS linked_account_user_id,  -- Renamed to avoid ambiguity
                la.social_network AS social_network,
                la.connection_link AS connection_link,
                la.connected_at AS connected_at,
                la.connection_reason AS connection_reason
            FROM users AS u
            LEFT JOIN linked_accounts AS la ON la.user_id = u.user_id
            WHERE u.user_id = :user_id
            """
        ).bindparams(user_id=user_id)

        result = await self.connection.execute(query)
        user = result.mappings().all()

        return convert_to_user_dto(user)
