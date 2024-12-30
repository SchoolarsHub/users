from dataclasses import dataclass
from uuid import UUID

from app.application.common.event_bus import EventBus
from app.application.common.unit_of_work import UnitOfWork
from app.domain.model.user.exceptions.user_exceptions import UserNotFoundError
from app.domain.model.user.repositories.user_repository import UserRepository
from app.domain.model.user.services.subscription_service import SubscriptionService


@dataclass(frozen=True)
class UnsubscrubeFromUserCommand:
    user_id: UUID
    subscribtioned_user_id: UUID


class UnsubscribeFromUser:
    def __init__(self, unit_of_work: UnitOfWork, subscription_service: SubscriptionService, event_bus: EventBus, repository: UserRepository) -> None:
        self.unit_of_work = unit_of_work
        self.subscription_service = subscription_service
        self.event_bus = event_bus
        self.repository = repository

    async def execute(self, command: UnsubscrubeFromUserCommand) -> None:
        user = await self.repository.with_id(uuid=command.user_id)

        if not user:
            raise UserNotFoundError(title=f"User with id: {command.user_id} does not exist")

        subscribtioned_user = await self.repository.with_id(uuid=command.subscribtioned_user_id)

        if not subscribtioned_user:
            raise UserNotFoundError(title=f"User with id: {command.subscribtioned_user_id} does not exist")

        await self.subscription_service.unsubscribe_from_user(subscriber=user, receiver=subscribtioned_user)
        await self.event_bus.publish(events=user.raise_events())
        await self.unit_of_work.commit()
