from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncConnection

from app.application.common.unit_of_work import UnitOfWork
from app.domain.model.user.user import User
from app.domain.model.user.value_objects import Contacts, Fullname
from app.infrastructure.databases.postgres.tables import linked_account_table, user_table


class UserFinder:
    def __init__(self, connection: AsyncConnection, unit_od_work: UnitOfWork) -> None:
        self.connection = connection
        self.unit_of_work = unit_od_work

    async def get_by_id(self, user_id: UUID) -> User | None:
        query = (
            select(user_table)
            .join(linked_account_table, user_table.c.user_id == linked_account_table.c.user_id, isouter=True)
            .where(user_table.c.user_id == user_id)
        )

        result = await self.connection.execute(query)
        user = result.unique().mappings().all()

        return self._map_to_entity(user) if user else None

    async def get_by_email(self, email: str) -> User | None:
        query = (
            select(user_table)
            .join(linked_account_table, user_table.c.user_id == linked_account_table.c.user_id, isouter=True)
            .where(user_table.c.email == email)
        )

        result = await self.connection.execute(query)
        user = result.unique().mappings().all()

        return self._map_to_entity(user) if user else None

    async def get_by_phone(self, phone: int) -> User | None:
        query = (
            select(user_table)
            .join(linked_account_table, user_table.c.user_id == linked_account_table.c.user_id, isouter=True)
            .where(user_table.c.phone == phone)
        )

        result = await self.connection.execute(query)
        user = result.unique().mappings().all()

        return self._map_to_entity(user) if user else None

    def _map_to_entity(self, user_dict: dict) -> User:
        # Create Fullname value object
        fullname = Fullname(firstname=user_dict["firstname"], lastname=user_dict["lastname"], middlename=user_dict["middlename"])

        # Create Contacts value object
        contacts = Contacts(email=user_dict["email"], phone=user_dict["phone"])

        # Create and return User entity
        return User(
            user_id=user_dict["user_id"],
            fullname=fullname,
            contacts=contacts,
            status=user_dict["status"],
            created_at=user_dict["created_at"],
            deleted_at=user_dict["deleted_at"],
            linked_accounts=[],  # Empty list since no linked accounts in the response
            unit_of_work=self.unit_of_work,
        )

    # Usage in your finder:
