from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from app.domain.model.avatar.avatar import Avatar


class AvatarRepositry(Protocol):
    @abstractmethod
    async def add(self, avatar: Avatar) -> None:
        raise NotImplementedError

    @abstractmethod
    async def with_id(self, avatar_id: UUID) -> Avatar | None:
        raise NotImplementedError
