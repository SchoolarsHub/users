from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from app.domain.model.linked_account.linked_account import LinkedAccount


class LinkedAccountRepository(Protocol):
    @abstractmethod
    async def with_id(self, linked_account_id: UUID) -> LinkedAccount | None:
        raise NotImplementedError

    @abstractmethod
    async def with_connection_link(self, connection_link: str) -> LinkedAccount | None:
        raise NotImplementedError
