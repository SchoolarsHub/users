from abc import abstractmethod
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Protocol


class Ioc(Protocol):
    @abstractmethod
    @asynccontextmanager
    async def provide[TProvidable](self, providable: type[TProvidable]) -> AsyncGenerator[TProvidable, None]:
        raise NotImplementedError
