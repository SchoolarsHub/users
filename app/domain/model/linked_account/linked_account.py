from datetime import UTC, datetime
from typing import Self
from uuid import UUID

from app.domain.model.linked_account.exceptions import ConnectionLinkNotBelongsToSocialNetworkError, InvalidSocialNetworkError
from app.domain.model.linked_account.social_networks import SocialNetworks
from app.domain.shared.base_entity import BaseEntity
from app.domain.shared.event import Event
from app.domain.shared.unit_of_work import UnitOfWorkTracker


class LinkedAccount(BaseEntity[UUID]):
    def __init__(
        self,
        linked_account_id: UUID,
        user_id: UUID,
        social_network: SocialNetworks,
        connection_link: str,
        unit_of_work: UnitOfWorkTracker,
        connected_at: datetime,
        connected_for: str | None,
    ) -> None:
        super().__init__(linked_account_id)

        self.unit_of_work = unit_of_work
        self.linked_account_id = linked_account_id
        self.social_network = social_network
        self.connection_link = connection_link
        self.connected_at = connected_at
        self.connected_for = connected_for
        self.user_id = user_id

        self._events: list[Event] = []

    def record_event(self, event: Event) -> None:
        self.events.append(event)

    def raise_events(self) -> list[Event]:
        events = self.events.copy()
        self.events.clear()

        return events

    @classmethod
    def create_linked_account(
        cls: type[Self],
        linked_account_id: UUID,
        user_id: UUID,
        social_network: SocialNetworks,
        connection_link: str,
        connected_for: str | None,
        unit_of_work: UnitOfWorkTracker,
    ) -> Self:
        if social_network not in connection_link:
            raise ConnectionLinkNotBelongsToSocialNetworkError(
                message=f"Connection link: {connection_link} not belongs to social network: {social_network}"
            )

        if social_network not in list(SocialNetworks):
            raise InvalidSocialNetworkError(message=f"Social network: {social_network} is invalid")

        linked_account = cls(linked_account_id, user_id, social_network, connection_link, unit_of_work, datetime.now(UTC), connected_for)
        unit_of_work.register_new(linked_account)

        return linked_account

    def change_connection_reason(self, connected_for: str) -> None:
        self.connected_for = connected_for
        self.unit_of_work.register_dirty(self)

    def delete_linked_account(self) -> None:
        self.unit_of_work.register_deleted(self)
