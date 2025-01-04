from dataclasses import dataclass
from uuid import UUID

from app.application.common.event_bus import EventBus
from app.application.common.unit_of_work import UnitOfWork
from app.domain.model.user.exceptions import UserNotFoundError
from app.domain.model.user.repository import UserRepository


@dataclass(frozen=True)
class UnlinkSocialNetworkCommand:
    user_id: UUID
    linked_account_id: UUID


class UnlinkSocialNetwork:
    def __init__(self, event_bus: EventBus, repository: UserRepository, unit_of_work: UnitOfWork) -> None:
        self.event_bus = event_bus
        self.repository = repository
        self.unit_of_work = unit_of_work

    async def execute(self, command: UnlinkSocialNetworkCommand) -> None:
        user = await self.repository.with_id(command.user_id)

        if not user:
            raise UserNotFoundError(message="User not found")

        user.unlink_social_network(command.linked_account_id)

        await self.event_bus.publish(events=user.raise_events())
        await self.unit_of_work.commit()
