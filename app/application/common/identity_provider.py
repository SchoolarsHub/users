from abc import abstractmethod
from typing import Protocol
from uuid import UUID


class IdentityProvider(Protocol):
    @abstractmethod
    async def get_current_user_id(self) -> UUID:
        raise NotImplementedError
