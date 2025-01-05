from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection

from app.application.common.unit_of_work import UnitOfWork
from app.domain.model.user.user import User


class UserFinder:
    def __init__(self, connection: AsyncConnection, unit_od_work: UnitOfWork) -> None:
        self.connection = connection
        self.unit_of_work = unit_od_work

    async def get_by_id(self, user_id: UUID) -> User | None:
        query = text(
            """
            SELECT
                u.user_id, u.firstname, u.lastname, u.middlename, u.email, u.phone, u.status, u.created_at, u.deleted_at,
                la.linked_account_id, la.user_id, la.social_network, la.connection_link, la.connected_at, la.connection_reason
            FROM users u
            INNER JOIN linked_accounts la ON u.user_id = la.user_id
            WHERE u.user_id = :user_id
            """
        ).bindparams(user_id=user_id)

        result = await self.connection.execute(query)
        user = result.unique().mappings().all()

        return user

    async def get_by_email(self, email: str) -> User | None:
        query = text(
            """
            SELECT
                u.user_id, u.firstname, u.lastname, u.middlename, u.email, u.phone, u.status, u.created_at, u.deleted_at,
                la.linked_account_id, la.user_id, la.social_network, la.connection_link, la.connected_at, la.connection_reason
            FROM users u
            INNER JOIN linked_accounts la ON u.user_id = la.user_id
            WHERE u.email = :email
            """
        ).bindparams(email=email)

        result = await self.connection.execute(query)
        user = result.unique().mappings().all()

        return user

    async def get_by_phone(self, phone: int) -> User | None:
        query = text(
            """
            SELECT
                u.user_id, u.firstname, u.lastname, u.middlename, u.email, u.phone, u.status, u.created_at, u.deleted_at,
                la.linked_account_id, la.user_id, la.social_network, la.connection_link, la.connected_at, la.connection_reason
            FROM users u
            INNER JOIN linked_accounts la ON u.user_id = la.user_id
            WHERE u.phone = :phone
            """
        ).bindparams(phone=phone)

        result = await self.connection.execute(query)
        user = result.unique().mappings().all()

        return user
