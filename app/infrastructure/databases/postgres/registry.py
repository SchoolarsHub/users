from app.domain.shared.base_entity import BaseEntity
from app.infrastructure.common.ioc import Ioc
from app.infrastructure.databases.postgres.gateways.generic_datamapper import GenericDataMapper


class Registry:
    def __init__(self, ioc: Ioc) -> None:
        self.ioc = ioc
        self.mappers: dict[type[BaseEntity], type[GenericDataMapper[BaseEntity]]] = {}

    async def get_mapper(self, entity: type[BaseEntity]) -> GenericDataMapper[BaseEntity]:
        mapper = self.mappers.get(entity)

        async with self.ioc.provide(mapper) as mapper_instance:
            return await mapper_instance

    def add_mapper(self, entity: type[BaseEntity], mapper: GenericDataMapper[BaseEntity]) -> None:
        self.mappers[entity] = mapper
