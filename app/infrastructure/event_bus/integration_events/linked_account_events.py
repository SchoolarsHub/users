from dataclasses import dataclass, field
from uuid import UUID

from app.domain.model.linked_account.events import ConnectionReasonChanged, LinkedAccountCreated, LinkedAccountDeleted
from app.domain.model.linked_account.social_networks import SocialNetworks
from app.infrastructure.event_bus.integration_events.integration_event import IntegrationEvent


@dataclass(frozen=True, kw_only=True)
class LinkedAccountCreatedIntegration(IntegrationEvent):
    linked_account_id: UUID
    social_network: SocialNetworks
    connected_for: str | None
    event_name: str = field(default="LinkedAccountCreated")

    @staticmethod
    def from_domain_event(event: LinkedAccountCreated) -> "LinkedAccountCreatedIntegration":
        return LinkedAccountCreatedIntegration(
            event_uuid=event.event_uuid,
            event_occured_at=event.event_occured_at,
            linked_account_id=event.linked_account_id,
            social_network=event.social_network,
            connected_for=event.connected_for,
        )


@dataclass(frozen=True, kw_only=True)
class ConnectionReasonChangedIntegration(IntegrationEvent):
    linked_account_id: UUID
    connected_for: str | None
    event_name: str = field(default="ConnectionReasonChanged")

    @staticmethod
    def from_domain_event(event: ConnectionReasonChanged) -> "ConnectionReasonChangedIntegration":
        return ConnectionReasonChangedIntegration(
            event_uuid=event.event_uuid,
            event_occured_at=event.event_occured_at,
            linked_account_id=event.linked_account_id,
            connected_for=event.connected_for,
        )


@dataclass(frozen=True, kw_only=True)
class LinkedAccountDeletedIntegration(IntegrationEvent):
    linked_account_id: UUID
    event_name: str = field(default="LinkedAccountDeleted")

    @staticmethod
    def from_domain_event(event: LinkedAccountDeleted) -> "LinkedAccountDeletedIntegration":
        return LinkedAccountDeletedIntegration(
            event_uuid=event.event_uuid,
            event_occured_at=event.event_occured_at,
            linked_account_id=event.linked_account_id,
        )
