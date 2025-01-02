from abc import abstractmethod
from typing import Protocol

from app.domain.shared.base_entity import BaseEntity


class UnitOfWorkTracker(Protocol):
    @abstractmethod
    def register_new(self, entity: BaseEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    def register_dirty(self, entity: BaseEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    def register_deleted(self, entity: BaseEntity) -> None:
        raise NotImplementedError
