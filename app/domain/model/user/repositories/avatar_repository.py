from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from app.domain.model.user.entities.avatar import Avatar


class AvatarRepository(Protocol):
    @abstractmethod
    async def with_id(self, uuid: UUID) -> Avatar | None:
        raise NotImplementedError

    @abstractmethod
    async def with_filename(self, filename: str) -> Avatar | None:
        raise NotImplementedError
