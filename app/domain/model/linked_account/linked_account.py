from datetime import UTC, datetime
from typing import Self
from uuid import UUID

from app.domain.model.linked_account.events import (
    ConnectionReasonChanged,
    LinkedAccountCreated,
    LinkedAccountDeleted,
)
from app.domain.model.linked_account.exceptions import ConnectionLinkNotBelongsToSocialNetworkError
from app.domain.model.linked_account.social_networks import SocialNetworks
from app.domain.shared.event import Event
from app.domain.shared.unit_of_work import UnitOfWorkTracker
from app.domain.shared.uowed_entity import UowedEntity


class LinkedAccount(UowedEntity[UUID]):
    def __init__(
        self,
        linked_account_id: UUID,
        social_network: SocialNetworks,
        connection_link: str,
        unit_of_work: UnitOfWorkTracker,
        connected_at: datetime,
        connected_for: str | None,
    ) -> None:
        super().__init__(linked_account_id, unit_of_work)

        self.linked_account_id = linked_account_id
        self.social_network = social_network
        self.connection_link = connection_link
        self.connected_at = connected_at
        self.connected_for = connected_for

        self._events: list[Event] = []

    def record_event[TEvent: Event](self, event: TEvent) -> None:
        self.events.append(event)

    def raise_events(self) -> list[Event]:
        events = self.events.copy()
        self.events.clear()

        return events

    @classmethod
    def create_linked_account(
        cls: type[Self],
        linked_account_id: UUID,
        social_network: SocialNetworks,
        connection_link: str,
        connected_for: str | None,
        unit_of_work: UnitOfWorkTracker,
    ) -> Self:
        if social_network not in connection_link:
            raise ConnectionLinkNotBelongsToSocialNetworkError(
                title=f"Connection link: {connection_link} not belongs to social network: {social_network}"
            )

        linked_account = cls(linked_account_id, social_network, connection_link, unit_of_work, datetime.now(UTC), connected_for)
        linked_account.mark_new()
        linked_account.record_event[LinkedAccountCreated](
            LinkedAccountCreated(linked_account_id, social_network, connected_for, linked_account.connected_at)
        )

        return linked_account

    def change_connection_reason(self, connected_for: str) -> None:
        self.connected_for = connected_for
        self.mark_dirty()
        self.record_event[ConnectionReasonChanged](ConnectionReasonChanged(self.linked_account_id, self.connected_for))

    def delete_linked_account(self) -> None:
        self.mark_deleted()
        self.record_event[LinkedAccountDeleted](LinkedAccountDeleted(self.linked_account_id))
