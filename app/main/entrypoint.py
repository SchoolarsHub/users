from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.main.di.main import setup_di
from app.main.di.providers import setup_async_container


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    yield


def app_factory() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    container = setup_async_container()

    setup_di(container=container, app=app)

    return app
