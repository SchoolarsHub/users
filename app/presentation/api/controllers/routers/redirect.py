from fastapi import APIRouter
from starlette import status
from starlette.responses import RedirectResponse

router = APIRouter()


@router.get("/")
async def redirect() -> RedirectResponse:
    return RedirectResponse(
        "/docs",
        status_code=status.HTTP_302_FOUND,
    )
