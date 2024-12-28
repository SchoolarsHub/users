from datetime import UTC, datetime
from typing import Self
from uuid import UUID

from app.domain.models.user.entities.avatar import Avatar
from app.domain.models.user.entities.linked_account import LinkedAccount
from app.domain.shared.event import Event
from app.domain.shared.unit_of_work import UnitOfWorkTracker
from app.domain.shared.uowed_entity import UowedEntity


class User(UowedEntity[UUID]):
    def __init__(
        self,
        user_id: UUID,
        username: str,
        created_at: datetime,
        unit_of_work: UnitOfWorkTracker,
        friends: list[Self],
        subscribers: list[Self],
        subscribed_to: list[Self],
        my_friendship_requests: list[Self],
        friendship_requests_to_me: list[Self],
        blocked_users: list[Self],
        avatars: list[Avatar],
        linked_accounts: list[LinkedAccount],
        bio: str | None = None,
    ) -> None:
        super().__init__(user_id, unit_of_work)

        self.username = username
        self.created_at = created_at
        self.frineds = friends
        self.subscribers = subscribers
        self.subscribed_to = subscribed_to
        self.my_friendship_requests = my_friendship_requests
        self.friendship_requests_to_me = friendship_requests_to_me
        self.blocked_users = blocked_users
        self.bio = bio
        self.avatars = avatars
        self.linked_accounts = linked_accounts

        self._events: list[Event] = []

    def record_event(self, event: Event) -> None:
        self._events.append(event)

    def raise_events(self) -> list[Event]:
        events = self._events.copy()
        self._events.clear()
        return events

    @classmethod
    def create_user(cls: type[Self], user_id: UUID, username: str, unit_of_work: UnitOfWorkTracker) -> Self:
        user = cls(user_id=user_id, username=username, created_at=datetime.now(UTC), unit_of_work=unit_of_work)
        user.mark_new()
        user.record_event(...)

        return user

    def change_username(self, username: str) -> None:
        self.username = username
        self.mark_dirty()
        self.record_event(...)

    def change_bio(self, bio: str | None = None) -> None:
        self.bio = bio
        self.mark_dirty()
        self.record_event(...)

    def delete_user(self) -> None:
        self.mark_deleted()
        self.record_event(...)
