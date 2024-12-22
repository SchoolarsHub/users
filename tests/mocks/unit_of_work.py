from app.domain.common.unit_of_work import UnitOfWorkTracker


class FakeUowTracker[EntityT](UnitOfWorkTracker):
    def __init__(self) -> None:
        self.dirty: dict[type[EntityT], EntityT] = {}
        self.new: dict[type[EntityT], EntityT] = {}
        self.deleted: dict[type[EntityT], EntityT] = {}

    def register_new(self, entity: EntityT) -> None:
        self.new[type(entity)] = entity

    def register_deleted(self, entity: EntityT) -> None:
        self.deleted[type(entity)] = entity

    def register_dirty(self, entity: EntityT) -> None:
        self.dirty[type(entity)] = entity
