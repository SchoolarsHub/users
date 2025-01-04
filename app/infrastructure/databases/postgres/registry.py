from typing import Any

from app.domain.shared.base_entity import BaseEntity
from app.infrastructure.databases.postgres.gateways.generic_datamapper import GenericDataMapper


class Registry:
    def __init__(self) -> None:
        self.mappers: dict[type[BaseEntity], type[GenericDataMapper[BaseEntity]]] = {}

    def get_mapper[TEntity: BaseEntity](self, entity: type[TEntity], *args: Any, **kwargs: Any) -> GenericDataMapper[TEntity]:
        requested_mapper = self.mappers.get(entity)
        return self._override_mapper(*args, mapper=requested_mapper, **kwargs)

    def add_mapper(self, entity: type[BaseEntity], mapper: type[GenericDataMapper[BaseEntity]]) -> None:
        self.mappers[entity] = mapper

    def _override_mapper[TEntity: BaseEntity](
        self, mapper: type[GenericDataMapper[TEntity]], *args: Any, **kwargs: Any
    ) -> GenericDataMapper[TEntity]:
        overrided_mapper = mapper(*args, **kwargs)
        return overrided_mapper
