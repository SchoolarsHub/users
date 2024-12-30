from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from app.domain.model.user.entities.user import User


class UserRepository(Protocol):
    @abstractmethod
    async def with_id(self, uuid: UUID) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def with_email(self, email: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def with_phone_number(self, phone_number: int) -> User | None:
        raise NotImplementedError
