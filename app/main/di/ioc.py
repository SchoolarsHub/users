from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from dishka import AsyncContainer

from app.infrastructure.common.ioc import Ioc


class DishkaIoc(Ioc):
    def __init__(self, container: AsyncContainer) -> None:
        self.container = container

    @asynccontextmanager
    async def provide[TProvidable](self, providable: type[TProvidable]) -> AsyncGenerator[TProvidable, None]:
        async with self.container() as req_container:
            yield await req_container.get(providable)
