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
        blocker.subscribers.remove(will_blocked)
        blocker.subscribed_to.remove(will_blocked)
        blocker.my_friendship_requests.remove(will_blocked)
        blocker.frineds.remove(will_blocked)
        blocker.friendship_requests_to_me.remove(will_blocked)

        will_blocked.subscribers.remove(blocker)
        will_blocked.subscribed_to.remove(blocker)
        will_blocked.my_friendship_requests.remove(blocker)
        will_blocked.frineds.remove(blocker)
        will_blocked.friendship_requests_to_me.remove(blocker)

    def unblock_user(self, blocker: User, blocked: User) -> None:
        if blocked not in blocker.blocked_users:
            raise BlockedUserNotFoundError(title=f"User {blocker.entity_id} does not block user {blocked.entity_id}")

        blocker.blocked_users.remove(blocked)
