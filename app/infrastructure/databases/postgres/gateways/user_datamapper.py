from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection

from app.domain.model.user.user import User
from app.infrastructure.databases.postgres.gateways.generic_datamapper import GenericDataMapper


class UserDataMapper(GenericDataMapper[User]):
    def __init__(self, connection: AsyncConnection) -> None:
        self.connection = connection

    async def save(self, entity: User) -> None:
        stmt = text(
            """
            INSERT INTO users (user_id, firstname, lastname, middlename, email, phone, status, created_at, deleted_at)
            VALUES (:user_id, :firstname, :lastname, :middlename, :email, :phone, :status, :created_at, :deleted_at)
            """
        ).bindparams(
            user_id=entity.user_id,
            firstname=entity.fullname.firstname,
            lastname=entity.fullname.lastname,
            middlename=entity.fullname.middlename,
            email=entity.contacts.email,
            phone=entity.contacts.phone,
            status=entity.status,
            created_at=entity.created_at,
            deleted_at=entity.deleted_at,
        )

        await self.connection.execute(stmt)

    async def update(self, entity: User) -> None:
        stmt = text(
            """
            UPDATE users
            SET firstname = :firstname,
                lastname = :lastname,
                middlename = :middlename,
                email = :email,
                phone = :phone,
                status = :status,
                created_at = :created_at,
                deleted_at = :deleted_at
            WHERE user_id = :user_id
            """
        ).bindparams(
            user_id=entity.user_id,
            firstname=entity.fullname.firstname,
            lastname=entity.fullname.lastname,
            middlename=entity.fullname.middlename,
            email=entity.contacts.email,
            phone=entity.contacts.phone,
            status=entity.status,
            created_at=entity.created_at,
            deleted_at=entity.deleted_at,
        )

        await self.connection.execute(stmt)

    async def delete(self, entity: User) -> None:
        stmt = text(
            """
            DELETE FROM users WHERE user_id = :user_id
            """
        ).bindparams(user_id=entity.user_id)

        await self.connection.execute(stmt)
