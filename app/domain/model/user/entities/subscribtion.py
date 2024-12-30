from datetime import UTC, datetime
from typing import Self
from uuid import UUID

from app.domain.shared.unit_of_work import UnitOfWorkTracker
from app.domain.shared.uowed_entity import UowedEntity


class Subscribtion(UowedEntity[UUID]):
    def __init__(
        self,
        subscription_id: UUID,
        unit_of_work: UnitOfWorkTracker,
        subscriber_id: UUID,
        subscribed_to: UUID,
        subscribed_at: datetime,
    ) -> None:
        super().__init__(subscription_id, unit_of_work)

        self.subscriber_id = subscriber_id
        self.subscribed_to = subscribed_to
        self.subscribed_at = subscribed_at

    @classmethod
    def create_subscribtion(
        cls: type[Self],
        subscriber_id: UUID,
        subscribed_to: UUID,
        subscription_id: UUID,
        unit_of_work: UnitOfWorkTracker,
    ) -> Self:
        subscribtion = cls(
            subscription_id=subscription_id,
            unit_of_work=unit_of_work,
            subscriber_id=subscriber_id,
            subscribed_to=subscribed_to,
            subscribed_at=datetime.now(UTC),
        )
        subscribtion.mark_new()

    def delete_subscription(self) -> None:
        self.mark_deleted()
