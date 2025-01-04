from dataclasses import dataclass, field

from fastapi import APIRouter
from starlette import status

from app.presentation.api.shemas.responses import SuccessResponse

router = APIRouter(tags=["Healthcheck"])


@dataclass(frozen=True)
class Healthcheck:
    status: str = field(default="OK")


@router.post(
    "/healthcheck",
    responses={status.HTTP_200_OK: {"model": SuccessResponse[Healthcheck]}},
    status_code=status.HTTP_200_OK,
)
async def healthcheck() -> SuccessResponse[Healthcheck]:
    return SuccessResponse(status=status.HTTP_200_OK, result=Healthcheck())
