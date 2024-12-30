from fastapi import FastAPI

from app.presentation.api.controllers.exception_handlers import default_error_handler
from app.presentation.api.controllers.routers import healthcheck, redirect
from app.presentation.api.middlewares.cors_middleware import setup_cors_middleware


def setup_routers(app: FastAPI) -> None:
    app.include_router(healthcheck.router, tags=["healthcheck"], prefix="/healthcheck")
    app.include_router(redirect.router, include_in_schema=False)


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(Exception, default_error_handler)


def setup_middlewares(app: FastAPI) -> None:
    setup_cors_middleware(app)
