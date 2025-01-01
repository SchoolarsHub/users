from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from app.application.common.dto.user_dto import UserDTO


class UserGateway(Protocol):
    @abstractmethod
    async def with_id(self, user_id: UUID) -> UserDTO | None:
        raise NotImplementedError
