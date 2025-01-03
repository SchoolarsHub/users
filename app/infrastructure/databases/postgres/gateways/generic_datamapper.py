from abc import abstractmethod
from typing import Protocol

from app.domain.shared.base_entity import BaseEntity


class GenericDataMapper[EntityT: BaseEntity](Protocol):
    @abstractmethod
    async def save(self, entity: EntityT) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, entity: EntityT) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, entity: EntityT) -> None:
        raise NotImplementedError
