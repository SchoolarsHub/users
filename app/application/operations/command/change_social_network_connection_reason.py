from dataclasses import dataclass
from uuid import UUID

from app.application.common.event_bus import EventBus
from app.application.common.unit_of_work import UnitOfWork
from app.domain.model.user.exceptions import UserNotFoundError
from app.domain.model.user.repository import UserRepository


@dataclass(frozen=True)
class ChangeSocialNetworkConnectionReasonCommand:
    user_id: UUID
    linked_account_id: UUID
    reason: str | None


class ChangeSocialNetworkConnectionReason:
    def __init__(self, repository: UserRepository, event_bus: EventBus, unit_of_work: UnitOfWork) -> None:
        self.repository = repository
        self.event_bus = event_bus
        self.unit_of_work = unit_of_work

    async def execute(self, command: ChangeSocialNetworkConnectionReasonCommand) -> None:
        user = await self.repository.with_id(command.user_id)

        if not user:
            raise UserNotFoundError(message="User not found")

        user.change_social_network_connection_reason(command.linked_account_id, command.reason)

        await self.event_bus.publish(events=user.raise_events())
        await self.unit_of_work.commit()
