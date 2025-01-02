from uuid import UUID

from app.application.common.unit_of_work import UnitOfWork
from app.domain.model.linked_account.linked_account import LinkedAccount
from app.domain.model.user.repository import UserRepository
from app.domain.model.user.user import User
from tests.mocks.database import FakeDatabase


class FakeUserRepository(UserRepository):
    def __init__(self, database: FakeDatabase, unit_of_work: UnitOfWork) -> None:
        self.database = database
        self.unit_of_work = unit_of_work

    async def add(self, user: User) -> None:
        self.unit_of_work.register_new(entity=user)

    async def update(self, user: User) -> None:
        self.unit_of_work.register_dirty(entity=user)

    async def delete(self, user: User) -> None:
        self.unit_of_work.register_deleted(entity=user)

    async def with_id(self, user_id: UUID) -> User | None:
        user = self.database.users.get(user_id)
        linked_accounts = self._get_linked_accounts(user_id=user.user_id)
        user.linked_accounts + linked_accounts

        return user

    async def with_email(self, email: str) -> User | None:
        for user in self.database.users.values():
            if user.contacts.email == email and email is not None:
                linked_accounts = self._get_linked_accounts(user_id=user.user_id)
                user.linked_accounts + linked_accounts

                return user

        return None

    async def with_phone(self, phone: int) -> None:
        for user in self.database.users.values():
            if user.contacts.phone == phone and phone is not None:
                linked_accounts = self._get_linked_accounts(user_id=user.user_id)
                user.linked_accounts + linked_accounts

                return user

        return None

    def _get_linked_accounts(self, user_id: UUID) -> list[LinkedAccount]:
        linked_accounts = [linked_account for linked_account in self.database.linked_accounts.values() if linked_account.user_id == user_id]

        return linked_accounts