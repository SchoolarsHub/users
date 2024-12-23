from app.domain.common.unit_of_work import UnitOfWorkTracker
from app.domain.common.uowed_entity import UowedEntity


class FakeUowTracker(UnitOfWorkTracker[UowedEntity]):
    def __init__(self) -> None:
        self.dirty: dict[type[UowedEntity], UowedEntity] = {}
        self.new: dict[type[UowedEntity], UowedEntity] = {}
        self.deleted: dict[type[UowedEntity], UowedEntity] = {}

    def register_new(self, entity: UowedEntity) -> None:
        self.new[type(entity)] = entity

    def register_deleted(self, entity: UowedEntity) -> None:
        self.deleted[type(entity)] = entity

    def register_dirty(self, entity: UowedEntity) -> None:
        self.dirty[type(entity)] = entity
