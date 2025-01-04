from dataclasses import dataclass
from uuid import UUID, uuid4

from app.application.common.event_bus import EventBus
from app.application.common.unit_of_work import UnitOfWork
from app.domain.model.linked_account.social_networks import SocialNetworks
from app.domain.model.user.exceptions import UserNotFoundError
from app.domain.model.user.repository import UserRepository


@dataclass(frozen=True)
class LinkSocialNetworkCommand:
    user_id: UUID
    social_network: SocialNetworks
    connection_link: str
    connected_for: str | None


class LinkSocialNetwork:
    def __init__(self, event_bus: EventBus, repository: UserRepository, unit_of_work: UnitOfWork) -> None:
        self.event_bus = event_bus
        self.repository = repository
        self.unit_of_work = unit_of_work

    async def execute(self, command: LinkSocialNetworkCommand) -> UUID:
        user = await self.repository.with_id(command.user_id)

        if not user:
            raise UserNotFoundError(message="User not found")

        linked_account_id = uuid4()
        user.link_social_network(linked_account_id, command.social_network, command.connection_link, command.connected_for)

        await self.event_bus.publish(events=user.raise_events())
        await self.unit_of_work.commit()

        return linked_account_id
