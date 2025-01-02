from app.domain.shared.base_entity import BaseEntity
from tests.mocks.user_mappers import GenericDataMapper


class Registry:
    def __init__(self) -> None:
        self.mappers: dict[type[BaseEntity], GenericDataMapper] = {}

    def get_mapper(self, entity: type[BaseEntity]) -> GenericDataMapper[BaseEntity]:
        return self.mappers.get(entity)

    def add_mapper(self, entity: type[BaseEntity], mapper: GenericDataMapper[BaseEntity]) -> None:
        self.mappers[entity] = mapper
