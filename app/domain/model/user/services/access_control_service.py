from uuid import UUID

from app.domain.model.user.entities.user import User
from app.domain.model.user.enums.account_statuses import AccountStatuses
from app.domain.model.user.exceptions.access_control_exceptions import (
    BlockedUserNotFoundError,
    CannotBlockUserTwiceError,
    CannotBlockYourselfError,
)
from app.domain.model.user.exceptions.user_exceptions import UserInactiveError, UserNotFoundError
from app.domain.model.user.repositories.user_repository import UserRepository


class AccessControlService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def block_user(self, blocker_id: UUID, will_blocked_user_id: UUID) -> None:
        if blocker_id == will_blocked_user_id:
            raise CannotBlockYourselfError(title="You cannot block yourself")

        blocker = await self.repository.with_id(blocker_id)
        will_blocked_user = await self.repository.with_id(will_blocked_user_id)

        if not blocker:
            raise UserNotFoundError(title=f"Blocker user with id: {blocker_id} not found")

        if not will_blocked_user:
            raise BlockedUserNotFoundError(title=f"Blocked user with id: {will_blocked_user_id} not found")

        if blocker.account_status == AccountStatuses.INACTIVE:
            raise UserInactiveError(title="You cannot block inactive user")

        if will_blocked_user.account_status == AccountStatuses.INACTIVE:
            raise UserInactiveError(title="You cannot block inactive user")

        if will_blocked_user.entity_id in blocker.blocked_users:
            raise CannotBlockUserTwiceError(title="You cannot block the same user twice")

        blocker.blocked_users.append(will_blocked_user.entity_id)

        self._terminate_relationships(blocker, will_blocked_user)
        self._terminate_relationships(will_blocked_user, blocker)

    async def unblock_user(self, blocker_id: UUID, blocked_user_id: UUID) -> None:
        if blocker_id == blocked_user_id:
            raise CannotBlockYourselfError(title="You cannot unblock yourself")

        blocker = await self.repository.with_id(blocker_id)
        blocked_user = await self.repository.with_id(blocked_user_id)

        if not blocker:
            raise UserNotFoundError(title=f"Blocker user with id: {blocker_id} not found")

        if not blocked_user:
            raise BlockedUserNotFoundError(title=f"Blocked user with id: {blocked_user_id} not found")

        if blocked_user.entity_id not in blocker.blocked_users:
            raise BlockedUserNotFoundError(title="Blocked user not found")

        blocker.blocked_users.remove(blocked_user.entity_id)

    def _terminate_relationships(self, user: User, target: User) -> None:
        relationships = [user.frineds, user.sended_friendship_requests, user.received_friendship_requests, user.subscribers, user.subscriptions]

        for relation in relationships:
            if target.entity_id in relation:
                relation.remove(target.entity_id)
