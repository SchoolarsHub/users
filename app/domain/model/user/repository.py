from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from app.domain.model.user.user import User


class UserRepository(Protocol):
    @abstractmethod
    def add(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    async def with_id(self, user_id: UUID) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def with_email(self, email: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def with_phone(self, phone: int) -> User | None:
        raise NotImplementedError
