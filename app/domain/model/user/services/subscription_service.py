from uuid import UUID

from app.domain.model.user.enums.account_statuses import AccountStatuses
from app.domain.model.user.exceptions.subscription_exceptions import (
    BlockedUserCannotSubscribeError,
    CannotSubscibeToBlockedUserError,
    CannotSubscibeToYourselfError,
    SubscriptionAlreadyExistsError,
    SubscriptionNotFoundError,
)
from app.domain.model.user.exceptions.user_exceptions import UserInactiveError, UserNotFoundError
from app.domain.model.user.repositories.user_repository import UserRepository


class SubscriptionService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    async def subscribe_to_user(self, subscriber_id: UUID, receiver_id: UUID) -> None:
        if subscriber_id == receiver_id:
            raise CannotSubscibeToYourselfError(title="Cannot subscribe to yourself")

        subscriber = await self.user_repository.with_id(subscriber_id)
        receiver = await self.user_repository.with_id(receiver_id)

        if not subscriber:
            raise UserNotFoundError(title="Subscriber not found")

        if not receiver:
            raise UserNotFoundError(title="Receiver not found")

        if subscriber.account_status == AccountStatuses.INACTIVE:
            raise BlockedUserCannotSubscribeError(title="Inactiver user cannot subscribe")

        if receiver.account_status == AccountStatuses.INACTIVE:
            raise CannotSubscibeToBlockedUserError(title="Cannot subscribe to inactive user")

        if receiver.entity_id in subscriber.subscriptions:
            raise SubscriptionAlreadyExistsError(title="Subscription already exists")

        subscriber.subscriptions.append(receiver.entity_id)
        receiver.subscribers.append(subscriber.entity_id)

    async def unsubscribe_from_user(self, subscriber_id: UUID, receiver_id: UUID) -> None:
        if subscriber_id == receiver_id:
            raise CannotSubscibeToYourselfError(title="Cannot unsubscribe from yourself")

        subscriber = await self.user_repository.with_id(subscriber_id)
        receiver = await self.user_repository.with_id(receiver_id)

        if not subscriber:
            raise UserNotFoundError(title="Subscriber not found")

        if not receiver:
            raise UserNotFoundError(title="Receiver not found")

        if subscriber.account_status == AccountStatuses.INACTIVE:
            raise UserInactiveError(title="Inactiver user cannot unsubscribe")

        if receiver.account_status == AccountStatuses.INACTIVE:
            raise UserInactiveError(title="Cannot unsubscribe from inactive user")

        if receiver.entity_id not in subscriber.subscriptions:
            raise SubscriptionNotFoundError(title="Subscription not found")

        subscriber.subscriptions.remove(receiver.entity_id)
        receiver.subscribers.remove(subscriber.entity_id)
