from abc import abstractmethod
from typing import Protocol

from app.domain.model.linked_account.linked_account import LinkedAccount
from app.domain.model.user.user import User
from app.domain.shared.base_entity import BaseEntity
from tests.mocks.database import FakeDatabase


class GenericDataMapper[EntityT: BaseEntity](Protocol):
    @abstractmethod
    async def save(self, entity: EntityT) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, entity: EntityT) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, entity: EntityT) -> None:
        raise NotImplementedError


class UserDataMapper(GenericDataMapper[User]):
    def __init__(self, database: FakeDatabase) -> None:
        self.database = database

    async def save(self, entity: User) -> None:
        self.database.users[entity.user_id] = entity

    async def update(self, entity: User) -> None:
        self.database.users[entity.user_id] = entity

    async def delete(self, entity: User) -> None:
        del self.database.users[entity.user_id]


class LinkedAccountDataMapper(GenericDataMapper[LinkedAccount]):
    def __init__(self, database: FakeDatabase) -> None:
        self.database = database

    async def save(self, entity: LinkedAccount) -> None:
        self.database.linked_accounts[entity.linked_account_id] = entity

    async def update(self, entity: LinkedAccount) -> None:
        self.database.linked_accounts[entity.linked_account_id] = entity

    async def delete(self, entity: LinkedAccount) -> None:
        del self.database.linked_accounts[entity.linked_account_id]
