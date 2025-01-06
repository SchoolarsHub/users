from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter
from starlette import status

from app.application.common.dto.user_dto import UserDTO
from app.application.operations.command.change_contacts import ChangeContacts, ChangeContactsCommand
from app.application.operations.command.change_fullname import ChangeFullname, ChangeFullnameCommand
from app.application.operations.command.change_social_network_connection_reason import (
    ChangeSocialNetworkConnectionReason,
    ChangeSocialNetworkConnectionReasonCommand,
)
from app.application.operations.command.create_user import CreateUser, CreateUserCommand
from app.application.operations.command.delete_user_permanently import DeleteUserPermanently, DeleteUserPermanentlyCommand
from app.application.operations.command.delete_user_temporarily import DeleteUserTemporarily, DeleteUserTemporarilyCommand
from app.application.operations.command.link_social_network import LinkSocialNetwork, LinkSocialNetworkCommand
from app.application.operations.command.recovery_user import RecoveryUser, RecoveryUserCommand
from app.application.operations.command.unlink_social_network import UnlinkSocialNetwork, UnlinkSocialNetworkCommand
from app.application.operations.query.get_user_by_id import GetUserById, GetUserByIdQuery
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
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorResponse[ContactsValidationError],
            "description": "Invalid contacts",
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
    "/change-contacts",
    responses={
        status.HTTP_200_OK: {
            "model": SuccessResponse,
            "description": "Contacts changed successfully",
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
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorResponse[ContactsValidationError],
            "description": "Invalid contacts",
        },
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def change_contacts(command: ChangeContactsCommand, handler: FromDishka[ChangeContacts]) -> SuccessResponse:
    await handler.execute(command=command)
    return SuccessResponse(status=status.HTTP_200_OK)


@router.post(
    "/link-social-network",
    responses={
        status.HTTP_201_CREATED: {
            "model": SuccessResponse[UUID],
            "description": "Social network linked successfully",
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
            "model": ErrorResponse[LinkedAccountAlreadyExistsError],
            "description": "Linked account already exists",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorResponse[InvalidSocialNetworkError],
            "description": "Invalid social network",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorResponse[ConnectionLinkNotBelongsToSocialNetworkError],
            "description": "Connection link not belongs to social network",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse[UserNotFoundError],
            "description": "User not found",
        },
    },
    status_code=status.HTTP_201_CREATED,
)
@inject
async def link_social_network(command: LinkSocialNetworkCommand, handler: FromDishka[LinkSocialNetwork]) -> SuccessResponse[UUID]:
    result = await handler.execute(command=command)
    return SuccessResponse(status=status.HTTP_201_CREATED, result=result)


@router.delete(
    "/unlink-social-network",
    responses={
        status.HTTP_200_OK: {
            "model": SuccessResponse,
            "description": "Social network unlinked successfully",
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
            "model": ErrorResponse[LinkedAccountNotExistsError],
            "description": "Linked account not exists",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse[UserNotFoundError],
            "description": "User not found",
        },
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def unlink_social_network(command: UnlinkSocialNetworkCommand, handler: FromDishka[UnlinkSocialNetwork]) -> SuccessResponse:
    await handler.execute(command=command)
    return SuccessResponse(status=status.HTTP_200_OK)


@router.put(
    "/change-social-network-connection-reason",
    responses={
        status.HTTP_200_OK: {
            "model": SuccessResponse,
            "description": "Social network connection reason changed successfully",
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
            "model": ErrorResponse[LinkedAccountNotExistsError],
            "description": "Linked account not exists",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse[UserNotFoundError],
            "description": "User not found",
        },
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def change_social_network_connection_reason(
    command: ChangeSocialNetworkConnectionReasonCommand, handler: FromDishka[ChangeSocialNetworkConnectionReason]
) -> SuccessResponse:
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
