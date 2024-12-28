from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from app.domain.models.user.entities.user import User


class UserRepository(Protocol):
    @abstractmethod
    async def with_id(self, uuid: UUID) -> User | None:
        raise NotImplementedError
