from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.presentation.api.main import setup_exception_handlers, setup_middlewares, setup_routers


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    yield


def app_factory() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    setup_routers(app)
    setup_middlewares(app)
    setup_exception_handlers(app)
    return app
