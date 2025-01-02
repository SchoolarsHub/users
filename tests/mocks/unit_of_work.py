from uuid import UUID

from app.application.common.unit_of_work import UnitOfWork
from app.domain.shared.base_entity import BaseEntity
from tests.mocks.registry import Registry


class FakeUnitOfWork(UnitOfWork):
    def __init__(self, registry: Registry) -> None:
        self.dirty: dict[UUID, BaseEntity] = {}
        self.new: dict[UUID, BaseEntity] = {}
        self.deleted: dict[UUID, BaseEntity] = {}
        self.registry = registry
        self.committed = False

    def register_deleted(self, entity: BaseEntity) -> None:
        if entity.entity_id in self.new:
            self.new.pop(entity.entity_id)

        if entity.entity_id in self.dirty:
            self.dirty.pop(entity.entity_id)

        self.deleted[entity.entity_id] = entity

    def register_dirty(self, entity: BaseEntity) -> None:
        if entity.entity_id in self.new:
            return
        self.dirty[entity.entity_id] = entity

    def register_new(self, entity: BaseEntity) -> None:
        self.new[entity.entity_id] = entity

    async def commit(self) -> None:
        for entity in self.new.values():
            mapper = self.registry.get_mapper(type(entity))
            await mapper.save(entity)

        for entity in self.dirty.values():
            mapper = self.registry.get_mapper(type(entity))
            await mapper.update(entity)

        for entity in self.deleted.values():
            mapper = self.registry.get_mapper(type(entity))
            await mapper.delete(entity)

        self.committed = True
