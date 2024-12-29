from dataclasses import dataclass
from uuid import UUID

from app.domain.models.user.enums.social_networks import SocialNetworks
from app.domain.shared.event import Event


@dataclass(frozen=True)
class SocialNetworkLinked(Event):
    user_id: UUID
    linked_account_id: UUID
    social_network_name: SocialNetworks
    connection_link: str
