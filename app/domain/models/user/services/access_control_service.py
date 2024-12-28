from app.domain.models.user.entities.user import User
from app.domain.models.user.exceptions.access_control_exceptions import (
    BlockedUserNotFoundError,
    CannotBlockUserTwiceError,
    CannotBlockYourselfError,
)


class AccessControlService:
    def block_user(self, blocker: User, will_blocked: User) -> None:
        if blocker.entity_id == will_blocked.entity_id:
            raise CannotBlockYourselfError(title=f"User {blocker.entity_id} cannot block himself")

        if will_blocked in blocker.blocked_users:
            raise CannotBlockUserTwiceError(
                title=f"User {blocker.entity_id} already blocked user {will_blocked.entity_id}"
            )

        blocker.blocked_users.append(will_blocked)

        self._remove_user_relational_data(blocker, will_blocked)
        self._remove_user_relational_data(will_blocked, blocker)

    def unblock_user(self, blocker: User, blocked: User) -> None:
        if blocked not in blocker.blocked_users:
            raise BlockedUserNotFoundError(title=f"User {blocker.entity_id} does not block user {blocked.entity_id}")

        blocker.blocked_users.remove(blocked)

    def _remove_user_relational_data(self, user: User, target: User) -> None:
        relationships = [
            user.subscribers,
            user.subscribed_to,
            user.my_friendship_requests,
            user.frineds,
            user.friendship_requests_to_me,
        ]

        for relationship in relationships:
            if target in relationship:
                relationship.remove(target)
