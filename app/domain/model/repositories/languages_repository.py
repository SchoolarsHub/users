from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from app.domain.model.entities.language import Language


class LanguagesRepository(Protocol):
    @abstractmethod
    def add(self, language: Language) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, language: Language) -> None:
        raise NotImplementedError

    @abstractmethod
    async def with_id(self, language_id: UUID) -> Language:
        raise NotImplementedError

    @abstractmethod
    async def with_user_id(self, user_id: UUID) -> list[Language]:
        raise NotImplementedError

    @abstractmethod
    async def with_language(self, language: str) -> list[Language]:
        raise NotImplementedError
