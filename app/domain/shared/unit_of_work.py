from abc import abstractmethod
from typing import Protocol


class UnitOfWorkTracker[EntityT](Protocol):
    @abstractmethod
    def register_new(self, entity: EntityT) -> None:
        raise NotImplementedError

    @abstractmethod
    def register_dirty(self, entity: EntityT) -> None:
        raise NotImplementedError

    @abstractmethod
    def register_deleted(self, entity: EntityT) -> None:
        raise NotImplementedError
