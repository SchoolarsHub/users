from uuid import UUID

from app.application.common.unit_of_work import UnitOfWork
from app.domain.model.user.repository import UserRepository
from app.domain.model.user.user import User
from app.infrastructure.databases.postgres.gateways.user_finder import UserFinder


class UserRepositoryImpl(UserRepository):
    def __init__(self, unit_of_work: UnitOfWork, user_finder: UserFinder) -> None:
        self.unit_of_work = unit_of_work
        self.user_finder = user_finder

    def add(self, user: User) -> None:
        self.unit_of_work.register_new(user)

    def delete(self, user: User) -> None:
        self.unit_of_work.register_deleted(user)

    def update(self, user: User) -> None:
        self.unit_of_work.register_dirty(user)

    async def with_id(self, user_id: UUID) -> User | None:
        return await self.user_finder.get_by_id(user_id)

    async def with_email(self, email: str) -> User | None:
        return await self.user_finder.get_by_email(email)

    async def with_phone(self, phone: int) -> User | None:
        return await self.user_finder.get_by_phone(phone)
