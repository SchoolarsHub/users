from functools import partial

from fastapi import FastAPI
from starlette import status

from app.domain.model.linked_account.exceptions import (
    ConnectionLinkNotBelongsToSocialNetworkError,
    InvalidSocialNetworkError,
    LinkedAccountAlreadyExistsError,
    LinkedAccountNotExistsError,
)
from app.domain.model.user.exceptions import (
    ContactsValidationError,
    InactiveUserError,
    UserAlreadyActiveError,
    UserAlreadyExistsError,
    UserNotFoundError,
    UserTemporarilyDeletedError,
)
from app.presentation.api.exc_handlers import domain_error_handler
from app.presentation.api.middlewares.cors_middleware import setup_cors_middleware
from app.presentation.api.routers import healthcheck, user


def setup_routers(app: FastAPI) -> None:
    app.include_router(healthcheck.router, prefix="/api/v1")
    app.include_router(user.router, prefix="/api/v1")


def setup_middlewares(app: FastAPI) -> None:
    setup_cors_middleware(app)


def setup_exc_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        UserAlreadyExistsError,
        partial(domain_error_handler, status_code=status.HTTP_409_CONFLICT),
    )
    app.add_exception_handler(
        UserAlreadyActiveError,
        partial(domain_error_handler, status_code=status.HTTP_400_BAD_REQUEST),
    )
    app.add_exception_handler(
        UserTemporarilyDeletedError,
        partial(domain_error_handler, status_code=status.HTTP_400_BAD_REQUEST),
    )
    app.add_exception_handler(
        InactiveUserError,
        partial(domain_error_handler, status_code=status.HTTP_400_BAD_REQUEST),
    )
    app.add_exception_handler(
        ConnectionLinkNotBelongsToSocialNetworkError,
        partial(domain_error_handler, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY),
    )
    app.add_exception_handler(
        InvalidSocialNetworkError,
        partial(domain_error_handler, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY),
    )
    app.add_exception_handler(
        LinkedAccountAlreadyExistsError,
        partial(domain_error_handler, status_code=status.HTTP_409_CONFLICT),
    )
    app.add_exception_handler(
        LinkedAccountNotExistsError,
        partial(domain_error_handler, status_code=status.HTTP_404_NOT_FOUND),
    )
    app.add_exception_handler(
        UserNotFoundError,
        partial(domain_error_handler, status_code=status.HTTP_404_NOT_FOUND),
    )
    app.add_exception_handler(
        ContactsValidationError,
        partial(domain_error_handler, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY),
    )
