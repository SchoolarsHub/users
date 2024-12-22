from dataclasses import dataclass, field

from fastapi import APIRouter
from starlette import status

from app.presentation.api.controllers.responses import SuccessfulResponse

router = APIRouter()


@dataclass
class HealthCheckData:
    title: str = field(default="OK")


@router.get(
    "/ensure-healthy",
    responses={
        status.HTTP_200_OK: {
            "model": SuccessfulResponse[HealthCheckData],
            "description": "Service is healthy",
        },
    },
    status_code=status.HTTP_200_OK,
)
async def get_status() -> SuccessfulResponse[HealthCheckData]:
    return SuccessfulResponse(status.HTTP_200_OK, HealthCheckData())
