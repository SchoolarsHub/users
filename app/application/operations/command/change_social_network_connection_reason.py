from dataclasses import dataclass
from uuid import UUID

from app.application.common.event_bus import EventBus
from app.application.common.identity_provider import IdentityProvider
from app.application.common.unit_of_work import UnitOfWork
from app.domain.model.user.repository import UserRepository


@dataclass(frozen=True)
class ChangeSocialNetworkConnectionReasonCommand:
    linked_account_id: UUID
    reason: str | None


class ChangeSocialNetworkConnectionReason:
    def __init__(self, repository: UserRepository, event_bus: EventBus, unit_of_work: UnitOfWork, identity_provider: IdentityProvider) -> None:
        self.repository = repository
        self.event_bus = event_bus
        self.unit_of_work = unit_of_work
        self.identity_provider = identity_provider

    async def execute(self, command: ChangeSocialNetworkConnectionReasonCommand) -> None:
        current_user_id = await self.identity_provider.get_current_user_id()

        user = await self.repository.with_id(current_user_id)

        user.change_social_network_connection_reason(command.linked_account_id, command.reason)

        await self.event_bus.publish(events=user.raise_events())
        await self.unit_of_work.commit()
