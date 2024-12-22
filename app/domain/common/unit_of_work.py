from typing import Protocol


class UnitOfWorkTracker[EntityT](Protocol):
    def register_new(self, entity: EntityT) -> None:
        raise NotImplementedError

    def register_dirty(self, entity: EntityT) -> None:
        raise NotImplementedError

    def register_deleted(self, entity: EntityT) -> None:
        raise NotImplementedError
