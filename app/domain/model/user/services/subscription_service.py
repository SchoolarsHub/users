from uuid import uuid4

from app.domain.model.user.entities.subscribtion import Subscribtion
from app.domain.model.user.entities.user import User
from app.domain.model.user.enums.account_statuses import AccountStatuses
from app.domain.model.user.exceptions.subscription_exceptions import (
    CannotSubscibeToYourselfError,
    CannotUnsubscribeFromYourselfError,
    SubscriptionAlreadyExistsError,
    SubscriptionNotFoundError,
)
from app.domain.model.user.exceptions.user_exceptions import UserInactiveError
from app.domain.shared.unit_of_work import UnitOfWorkTracker


class SubscriptionService:
    def __init__(self, unit_of_work: UnitOfWorkTracker) -> None:
        self.unit_of_work = unit_of_work

    async def subscribe_to_user(self, subscriber: User, receiver: User) -> None:
        if subscriber.entity_id == receiver.entity_id:
            raise CannotSubscibeToYourselfError(title="You cannot subscribe to yourself")

        if subscriber.account_status == AccountStatuses.INACTIVE:
            raise UserInactiveError(title="Subscriber is inactive")

        for subscription in subscriber.subscriptions:
            if subscription.subscribed_to == receiver.entity_id:
                raise SubscriptionAlreadyExistsError(title="Subscription already exists")

        subscription = Subscribtion.create_subscribtion(
            subscriber_id=subscriber.entity_id, receiver_id=receiver.entity_id, subscription_id=uuid4(), unit_of_work=self.unit_of_work
        )

        subscriber.subscriptions.append(subscription)
        receiver.subscribers.append(subscription)

    async def unsubscribe_from_user(self, subscriber: User, receiver: User) -> None:
        if subscriber.entity_id == receiver.entity_id:
            raise CannotUnsubscribeFromYourselfError(title="You cannot subscribe to yourself")

        if subscriber.account_status == AccountStatuses.INACTIVE:
            raise UserInactiveError(title="Subscriber is inactive")

        for subscription in subscriber.subscriptions:
            if subscription.subscribed_to == receiver.entity_id:
                subscriber.subscriptions.remove(subscription)
                receiver.subscribers.remove(subscription)

                subscription.delete_subscription()

        raise SubscriptionNotFoundError(title="Subscription not found")

    async def remove_from_subscribers(self, subscriber: User, receiver: User) -> None:
        if subscriber.entity_id == receiver.entity_id:
            raise CannotUnsubscribeFromYourselfError(title="You cannot subscribe to yourself")

        if receiver.account_status == AccountStatuses.INACTIVE:
            raise UserInactiveError(title="Receiver is inactive")

        for subscribed_user in receiver.subscribers:
            if subscribed_user.subscriber_id == subscriber.entity_id:
                receiver.subscribers.remove(subscriber)
                subscriber.subscriptions.remove(subscriber)

                subscriber.delete_subscription()

        raise SubscriptionNotFoundError(title="Subscription not found")
