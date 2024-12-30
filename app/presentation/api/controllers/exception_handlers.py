from fastapi import Request
from fastapi.responses import JSONResponse
from starlette import status

from app.application.common.exception import ApplicationError
from app.domain.shared.exception import DomainError
from app.presentation.api.controllers.responses import Data, ErrorResponse


async def domain_error_handler(request: Request, error: DomainError, status_code: int) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=ErrorResponse(
            status=status_code,
            error=Data(
                data=error,
                message=error.message,
            ),
        ),
    )


async def application_error_handler(request: Request, error: ApplicationError, status_code: int) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=ErrorResponse(
            status=status_code,
            error=Data(
                data=error,
                message=error.message,
            ),
        ),
    )


async def default_error_handler(request: Request, error: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error=Data(
                data=error,
            ),
        ),
    )
