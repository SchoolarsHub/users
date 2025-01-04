from dataclasses import asdict

from fastapi import Request
from fastapi.responses import JSONResponse

from app.domain.shared.exception import DomainError
from app.presentation.api.shemas.responses import ErrorData, ErrorResponse


async def domain_error_handler(request: Request, exc: DomainError, status: int) -> JSONResponse:
    return JSONResponse(status_code=status, content=asdict(ErrorResponse(status=status, error=ErrorData(title=exc.message))))
