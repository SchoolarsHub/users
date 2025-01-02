from app.application.common.unit_of_work import UnitOfWork
from app.domain.shared.base_entity import BaseEntity
from tests.mocks.registry import Registry


class FakeUnitOfWork(UnitOfWork):
    def __init__(self, registry: Registry) -> None:
        self.dirty: dict[type[BaseEntity], BaseEntity] = {}
        self.new: dict[type[BaseEntity], BaseEntity] = {}
        self.deleted: dict[type[BaseEntity], BaseEntity] = {}
        self.registry = registry
        self.committed = False

    def register_deleted(self, entity: BaseEntity) -> None:
        self.deleted[type(entity)] = entity

    def register_dirty(self, entity: BaseEntity) -> None:
        self.dirty[type(entity)] = entity

    def register_new(self, entity: BaseEntity) -> None:
        self.new[type(entity)] = entity

    async def commit(self) -> None:
        for entity_type, entity in self.new.items():
            mapper = self.registry.get_mapper(entity_type)
            await mapper.save(entity)

        for entity_type, entity in self.dirty.items():
            mapper = self.registry.get_mapper(entity_type)
            await mapper.update(entity)

        for entity_type, entity in self.deleted.items():
            mapper = self.registry.get_mapper(entity_type)
            await mapper.delete(entity)

        self.committed = True
