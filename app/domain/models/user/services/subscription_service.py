from app.domain.models.user.entities.user import User
from app.domain.models.user.exceptions.subscription_exceptions import (
    BlockedUserCannotSubscribeError,
    CannotSubscibeToBlockedUserError,
    CannotSubscibeToYourselfError,
    SubscriptionAlreadyExistsError,
    SubscriptionNotFoundError,
)


class SubscriptionService:
    def subsctibe_to_user(self, subscriber: User, receiver: User) -> None:
        if subscriber.entity_id == receiver.entity_id:
            raise CannotSubscibeToYourselfError(CannotSubscibeToYourselfError(title="Can not subscribe to yourself"))

        if receiver in subscriber.blocked_users:
            raise CannotSubscibeToBlockedUserError(title="Can not subscribe to blocked user")

        if subscriber in receiver.blocked_users:
            raise BlockedUserCannotSubscribeError(
                title=f"User with id: {receiver.entity_id} block you, can not subscribe"
            )

        if receiver in subscriber.subscribed_to:
            raise SubscriptionAlreadyExistsError(title=f"User with id: {receiver.entity_id} already subscribed")

        subscriber.subscribed_to.append(receiver)
        receiver.subscribers.append(receiver)

    def unsubscribe_from_user(self, subscriber: User, receiver: User) -> None:
        if receiver not in subscriber.subscribed_to:
            raise SubscriptionNotFoundError(title=f"User with id: {receiver.entity_id} not subscribed")

        subscriber.subscribed_to.remove(receiver)
        receiver.subscribers.remove(subscriber)
