from abc import abstractmethod
from typing import Protocol

from app.domain.common.unit_of_work import UnitOfWorkTracker


class UnitOfWorkCommiter(Protocol):
    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError


class UnitOfWork(UnitOfWorkTracker, UnitOfWorkCommiter):
    pass
