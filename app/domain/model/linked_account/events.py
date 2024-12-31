from dataclasses import dataclass
from uuid import UUID

from app.domain.model.linked_account.social_networks import SocialNetworks
from app.domain.shared.event import Event


@dataclass(frozen=True)
class LinkedAccountCreated(Event):
    linked_account_id: UUID
    social_network: SocialNetworks
    connected_for: str | None


@dataclass(frozen=True)
class ConnectionReasonChanged(Event):
    linked_account_id: UUID
    connected_for: str | None


@dataclass(frozen=True)
class LinkedAccountDeleted(Event):
    linked_account_id: UUID
