from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from app.domain.model.user.statuses import Statuses


class IdentityProvider(Protocol):
    @abstractmethod
    async def get_current_user_id(self) -> UUID:
        raise NotImplementedError

    @abstractmethod
    async def get_current_user_status(self) -> Statuses:
        raise NotImplementedError
