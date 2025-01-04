from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.main.di.main import setup_di
from app.main.di.providers import setup_async_container
from app.presentation.api.main import setup_exc_handlers, setup_middlewares, setup_routers


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    yield


def app_factory() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    container = setup_async_container()

    setup_di(container=container, app=app)
    setup_exc_handlers(app=app)
    setup_middlewares(app=app)
    setup_routers(app=app)

    return app
