from app.domain.shared.base_entity import BaseEntity
from app.infrastructure.databases.postgres.gateways.generic_datamapper import GenericDataMapper


class Registry:
    def __init__(self) -> None:
        self.mappers: dict[type[BaseEntity], GenericDataMapper[BaseEntity]] = {}

    def get_mapper(self, entity: type[BaseEntity]) -> GenericDataMapper[BaseEntity]:
        return self.mappers.get(entity)

    def add_mapper(self, entity: type[BaseEntity], mapper: GenericDataMapper[BaseEntity]) -> None:
        self.mappers[entity] = mapper
