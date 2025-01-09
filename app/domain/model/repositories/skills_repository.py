from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from app.domain.model.entities.skill import Skill


class SkillsRepository(Protocol):
    @abstractmethod
    def add(self, skill: Skill) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, skill: Skill) -> None:
        raise NotImplementedError

    @abstractmethod
    async def with_id(self, skill_id: UUID) -> Skill | None:
        raise NotImplementedError

    @abstractmethod
    async def with_user_id(self, user_id: UUID) -> list[Skill]:
        raise NotImplementedError

    @abstractmethod
    async def with_skill(self, skill: str) -> list[Skill]:
        raise NotImplementedError
