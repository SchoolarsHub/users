from uuid import UUID, uuid4

from app.domain.model.user.entities.subscribtion import Subscribtion
from app.domain.model.user.enums.account_statuses import AccountStatuses
from app.domain.model.user.exceptions.subscription_exceptions import (
    CannotSubscibeToYourselfError,
    CannotUnsubscribeFromYourselfError,
    SubscriptionAlreadyExistsError,
    SubscriptionNotFoundError,
)
from app.domain.model.user.exceptions.user_exceptions import UserInactiveError, UserNotFoundError
from app.domain.model.user.repositories.user_repository import UserRepository
from app.domain.shared.unit_of_work import UnitOfWorkTracker


class SubscriptionService:
    def __init__(self, user_repository: UserRepository, unit_of_work: UnitOfWorkTracker) -> None:
        self.user_repository = user_repository
        self.unit_of_work = unit_of_work

    async def subscribe_to_user(self, subscriber_id: UUID, receiver_id: UUID) -> None:
        if subscriber_id == receiver_id:
            raise CannotSubscibeToYourselfError(title="You cannot subscribe to yourself")

        subscriber = await self.user_repository.with_id(subscriber_id)
        receiver_subscription = await self.user_repository.with_id(receiver_id)

        if not subscriber:
            raise UserNotFoundError(title="Subscriber not found")

        if not receiver_subscription:
            raise UserNotFoundError(title="Receiver not found")

        if subscriber.account_status == AccountStatuses.INACTIVE:
            raise UserInactiveError(title="Subscriber is inactive")

        for subscription in subscriber.subscriptions:
            if subscription.subscribed_to == receiver_subscription.entity_id:
                raise SubscriptionAlreadyExistsError(title="Subscription already exists")

        subscription = Subscribtion.create_subscribtion(
            subscriber_id=subscriber.entity_id, receiver_id=receiver_subscription.entity_id, subscription_id=uuid4(), unit_of_work=self.unit_of_work
        )

        subscriber.subscriptions.append(subscription)
        receiver_subscription.subscribers.append(subscription)

    async def unsubscribe_from_user(self, subscriber_id: UUID, receiver_id: UUID) -> None:
        if subscriber_id == receiver_id:
            raise CannotUnsubscribeFromYourselfError(title="You cannot unsubscribe from yourself")

        subscriber = await self.user_repository.with_id(subscriber_id)
        receiver_subscription = await self.user_repository.with_id(receiver_id)

        if not subscriber:
            raise UserNotFoundError(title="Subscriber not found")

        if not receiver_subscription:
            raise UserNotFoundError(title="Receiver not found")

        if subscriber.account_status == AccountStatuses.INACTIVE:
            raise UserInactiveError(title="Subscriber is inactive")

        for subscription in subscriber.subscriptions:
            if subscription.subscribed_to == receiver_subscription.entity_id:
                subscriber.subscriptions.remove(subscription)
                receiver_subscription.subscribers.remove(subscription)

                subscription.delete_subscription()

        raise SubscriptionNotFoundError(title="Subscription not found")

    async def remove_from_subscribers(self, subscriber_id: UUID, receiver_id: UUID) -> None:
        if subscriber_id == receiver_id:
            raise CannotUnsubscribeFromYourselfError(title="You cannot unsubscribe from yourself")

        subscriber_to_user = await self.user_repository.with_id(subscriber_id)
        receiver_subscription = await self.user_repository.with_id(receiver_id)

        if not subscriber_to_user:
            raise UserNotFoundError(title="Subscriber not found")

        if not receiver_subscription:
            raise UserNotFoundError(title="Receiver not found")

        if receiver_subscription.account_status == AccountStatuses.INACTIVE:
            raise UserInactiveError(title="Receiver is inactive")

        for subscriber in receiver_subscription.subscribers:
            if subscriber.subscriber_id == subscriber.entity_id:
                receiver_subscription.subscribers.remove(subscriber)
                subscriber_to_user.subscriptions.remove(subscriber)

                subscriber.delete_subscription()

        raise SubscriptionNotFoundError(title="Subscription not found")
