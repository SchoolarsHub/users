from typing import Self
from uuid import UUID

from app.domain.common.unit_of_work import UnitOfWorkTracker


class UowedEntity[EntityId: UUID]:
    def __init__(self, entity_id: EntityId, unit_of_work: UnitOfWorkTracker[Self]) -> None:
        self.entity_id = entity_id
        self.unit_of_work = unit_of_work

    def mark_new(self) -> None:
        self.unit_of_work.register_new(self)

    def mark_dirty(self) -> None:
        self.unit_of_work.register_dirty(self)

    def mark_deleted(self) -> None:
        self.unit_of_work.register_deleted(self)
