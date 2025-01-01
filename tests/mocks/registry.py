from app.domain.shared.uowed_entity import UowedEntity
from tests.mocks.user_mappers import GenericDataMapper


class Registry:
    def __init__(self) -> None:
        self.mappers: dict[type[UowedEntity], GenericDataMapper] = {}

    def get_mapper(self, entity: type[UowedEntity]) -> GenericDataMapper[UowedEntity]:
        return self.mappers.get(entity)

    def add_mapper(self, entity: type[UowedEntity], mapper: GenericDataMapper[UowedEntity]) -> None:
        self.mappers[entity] = mapper
