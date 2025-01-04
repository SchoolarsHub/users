from sqlalchemy import delete, insert, update
from sqlalchemy.ext.asyncio import AsyncConnection

from app.domain.model.user.user import User
from app.infrastructure.databases.postgres.gateways.generic_datamapper import GenericDataMapper
from app.infrastructure.databases.postgres.tables import user_table


class UserDataMapper(GenericDataMapper[User]):
    def __init__(self, connection: AsyncConnection) -> None:
        self.connection = connection

    async def save(self, entity: User) -> None:
        stmt = insert(user_table).values(
            user_id=entity.user_id,
            firstname=entity.fullname.firstname,
            lastname=entity.fullname.lastname,
            middlename=entity.fullname.middlename,
            email=entity.contacts.email,
            phone=entity.contacts.phone,
            created_at=entity.created_at,
            deleted_at=entity.deleted_at,
            status=entity.status,
        )

        await self.connection.execute(stmt)

    async def update(self, entity: User) -> None:
        stmt = (
            update(user_table)
            .where(user_table.c.user_id == entity.user_id)
            .values(
                firstname=entity.fullname.firstname,
                lastname=entity.fullname.lastname,
                middlename=entity.fullname.middlename,
                email=entity.contacts.email,
                phone=entity.contacts.phone,
                created_at=entity.created_at,
                deleted_at=entity.deleted_at,
                status=entity.status,
            )
        )

        await self.connection.execute(stmt)

    async def delete(self, entity: User) -> None:
        stmt = delete(user_table).where(user_table.c.user_id == entity.user_id)

        await self.connection.execute(stmt)
