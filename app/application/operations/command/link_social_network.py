from dataclasses import dataclass
from uuid import UUID, uuid4

from app.application.common.event_bus import EventBus
from app.application.common.identity_provider import IdentityProvider
from app.application.common.unit_of_work import UnitOfWork
from app.domain.model.linked_account.social_networks import SocialNetworks
from app.domain.model.user.exceptions import UserNotFoundError
from app.domain.model.user.repository import UserRepository


@dataclass(frozen=True)
class LinkSocialNetworkCommand:
    social_network: SocialNetworks
    connection_link: str
    connected_for: str | None


class LinkSocialNetwork:
    def __init__(self, event_bus: EventBus, repository: UserRepository, unit_of_work: UnitOfWork, identity_provider: IdentityProvider) -> None:
        self.event_bus = event_bus
        self.repository = repository
        self.unit_of_work = unit_of_work
        self.identity_provider = identity_provider

    async def execute(self, command: LinkSocialNetworkCommand) -> UUID:
        current_user_id = await self.identity_provider.get_current_user_id()

        user = await self.repository.with_id(current_user_id)

        if not user:
            raise UserNotFoundError(title=f"User with id: {current_user_id} not found")

        linked_account_id = uuid4()
        user.link_social_network(linked_account_id, command.social_network, command.connection_link, command.connected_for)

        await self.event_bus.publish(events=user.raise_events())
        await self.unit_of_work.commit()

        return linked_account_id
