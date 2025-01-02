from uuid import UUID


class BaseEntity[EntityId: UUID]:
    def __init__(self, entity_id: EntityId) -> None:
        self.entity_id = entity_id
