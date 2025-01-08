from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter
from starlette import status

from app.application.common.dto.user_dto import UserDTO
from app.application.operations.command.user.change_email import ChangeEmail, ChangeEmailCommand
from app.application.operations.command.user.change_fullname import ChangeFullname, ChangeFullnameCommand
from app.application.operations.command.user.create_user import CreateUser, CreateUserCommand
from app.application.operations.command.user.delete_user_permanently import DeleteUserPermanently, DeleteUserPermanentlyCommand
from app.application.operations.command.user.delete_user_temporarily import DeleteUserTemporarily, DeleteUserTemporarilyCommand
from app.application.operations.command.user.recovery_user import RecoveryUser, RecoveryUserCommand
from app.application.operations.query.get_user_by_id import GetUserById, GetUserByIdQuery
from app.domain.model.user.exceptions import (
    InactiveUserError,
    UserAlreadyActiveError,
    UserAlreadyExistsError,
    UserNotFoundError,
    UserTemporarilyDeletedError,
)
from app.presentation.api.shemas.responses import ErrorResponse, SuccessResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/create_user",
    responses={
        status.HTTP_201_CREATED: {
            "model": SuccessResponse[UUID],
            "description": "User created successfully",
        },
        status.HTTP_409_CONFLICT: {
            "model": ErrorResponse[UserAlreadyExistsError],
            "description": "User already exists",
        },
    },
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_user(command: CreateUserCommand, handler: FromDishka[CreateUser]) -> SuccessResponse[UUID]:
    result = await handler.execute(command=command)
    return SuccessResponse(status=status.HTTP_201_CREATED, result=result)


@router.put(
    "/recovery-user",
    responses={
        status.HTTP_200_OK: {
            "model": SuccessResponse,
            "description": "User recovery successfully",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse[InactiveUserError],
            "description": "User is inactive",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse[UserAlreadyActiveError],
            "description": "User already active",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse[UserNotFoundError],
            "description": "User not found",
        },
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def recovery_user(command: RecoveryUserCommand, handler: FromDishka[RecoveryUser]) -> SuccessResponse:
    await handler.execute(command=command)
    return SuccessResponse(status=status.HTTP_200_OK)


@router.delete(
    "/delete-user-permanently",
    responses={
        status.HTTP_200_OK: {
            "model": SuccessResponse,
            "description": "User deleted successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse[UserNotFoundError],
            "description": "User not found",
        },
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def delete_user_permanently(command: DeleteUserPermanentlyCommand, handler: FromDishka[DeleteUserPermanently]) -> SuccessResponse:
    await handler.execute(command=command)
    return SuccessResponse(status=status.HTTP_200_OK)


@router.delete(
    "/delete-user-temporarily",
    responses={
        status.HTTP_200_OK: {
            "model": SuccessResponse,
            "description": "User deleted successfully",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse[InactiveUserError],
            "description": "User is inactive",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse[UserTemporarilyDeletedError],
            "description": "User already temporarily deleted",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse[UserNotFoundError],
            "description": "User not found",
        },
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def delete_user_temporarily(command: DeleteUserTemporarilyCommand, handler: FromDishka[DeleteUserTemporarily]) -> SuccessResponse:
    await handler.execute(command=command)
    return SuccessResponse(status=status.HTTP_200_OK)


@router.put(
    "/change-fullname",
    responses={
        status.HTTP_200_OK: {
            "model": SuccessResponse,
            "description": "Fullname changed successfully",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse[InactiveUserError],
            "description": "User is inactive",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse[UserTemporarilyDeletedError],
            "description": "User is temporarily deleted",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse[UserNotFoundError],
            "description": "User not found",
        },
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def change_fullname(command: ChangeFullnameCommand, handler: FromDishka[ChangeFullname]) -> SuccessResponse:
    await handler.execute(command=command)
    return SuccessResponse(status=status.HTTP_200_OK)


@router.put(
    "/change-email",
    responses={
        status.HTTP_200_OK: {
            "model": SuccessResponse,
            "description": "Email changed successfully",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse[InactiveUserError],
            "description": "User is inactive",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse[UserTemporarilyDeletedError],
            "description": "User is temporarily deleted",
        },
        status.HTTP_409_CONFLICT: {
            "model": ErrorResponse[UserAlreadyExistsError],
            "description": "User already exists",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse[UserNotFoundError],
            "description": "User not found",
        },
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def change_email(command: ChangeEmailCommand, handler: FromDishka[ChangeEmail]) -> SuccessResponse:
    await handler.execute(command=command)
    return SuccessResponse(status=status.HTTP_200_OK)


@router.get(
    "/{user_id}",
    responses={
        status.HTTP_200_OK: {
            "model": SuccessResponse[UserDTO | None],
            "description": "User found successfully",
        },
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def get_user_by_id(user_id: UUID, handler: FromDishka[GetUserById]) -> SuccessResponse[UserDTO | None]:
    query = GetUserByIdQuery(user_id=user_id)
    result = await handler.execute(query=query)
    return SuccessResponse(status=status.HTTP_200_OK, result=result)
