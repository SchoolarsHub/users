from dataclasses import dataclass, field
from uuid import UUID

from app.domain.model.linked_account.social_networks import SocialNetworks
from app.infrastructure.event_bus.integration_events.integration_event import IntegrationEvent


@dataclass(frozen=True)
class LinkedAccountCreatedIntegration(IntegrationEvent):
    linked_account_id: UUID
    social_network: SocialNetworks
    connected_for: str | None
    event_name: str = field(default="LinkedAccountCreated")


@dataclass(frozen=True)
class ConnectionReasonChangedIntegration(IntegrationEvent):
    linked_account_id: UUID
    connected_for: str | None
    event_name: str = field(default="ConnectionReasonChanged")


@dataclass(frozen=True)
class LinkedAccountDeletedIntegration(IntegrationEvent):
    linked_account_id: UUID
    event_name: str = field(default="LinkedAccountDeleted")
