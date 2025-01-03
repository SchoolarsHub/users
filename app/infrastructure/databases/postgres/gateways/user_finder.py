from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncConnection

from app.domain.model.linked_account.linked_account import LinkedAccount
from app.domain.model.user.user import User


class UserFinder:
    def __init__(self, connection: AsyncConnection) -> None:
        self.connection = connection

    async def get_by_id(self, user_id: UUID) -> User | None:
        query = select(User).join(LinkedAccount, User.user_id == LinkedAccount.user_id, isouter=True).where(User.user_id == user_id)

        result = await self.connection.execute(query)
        user = result.scalar_one_or_none()

        return user

    async def get_by_email(self, email: str) -> User | None:
        query = select(User).join(LinkedAccount, User.user_id == LinkedAccount.user_id, isouter=True).where(User.contacts.email == email)

        result = await self.connection.execute(query)
        user = result.scalar_one_or_none()

        return user

    async def get_by_phone(self, phone: int) -> User | None:
        query = select(User).join(LinkedAccount, User.user_id == LinkedAccount.user_id, isouter=True).where(User.contacts.phone == phone)

        result = await self.connection.execute(query)
        user = result.scalar_one_or_none()

        return user
