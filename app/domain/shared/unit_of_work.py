from abc import abstractmethod
from typing import Any, Protocol


class UnitOfWorkTracker(Protocol):
    @abstractmethod
    def register_new(self, entity: Any) -> None:
        raise NotImplementedError

    @abstractmethod
    def register_dirty(self, entity: Any) -> None:
        raise NotImplementedError

    @abstractmethod
    def register_deleted(self, entity: Any) -> None:
        raise NotImplementedError
