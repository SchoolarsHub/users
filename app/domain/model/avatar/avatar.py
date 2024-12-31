from datetime import UTC, datetime
from typing import Self
from uuid import UUID

from app.domain.model.avatar.events import AvatarCreated, AvatarDeleted
from app.domain.model.avatar.extensions import Extensions
from app.domain.model.avatar.value_objects import FileData
from app.domain.shared.event import Event
from app.domain.shared.unit_of_work import UnitOfWorkTracker
from app.domain.shared.uowed_entity import UowedEntity


class Avatar(UowedEntity[UUID]):
    def __init__(
        self,
        avatar_id: UUID,
        unit_of_work: UnitOfWorkTracker,
        content: bytes,
        file_data: FileData,
        created_at: datetime,
    ) -> None:
        super().__init__(avatar_id, unit_of_work)

        self.avatar_id = avatar_id
        self.content = content
        self.file_data = file_data
        self.created_at = created_at

        self._events: list[Event] = []

    def record_event[TEvent: Event](self, event: TEvent) -> None:
        self._events.append(event)

    def raise_events(self) -> list[Event]:
        events = self._events.copy()
        self._events.clear()

        return events

    @classmethod
    def create_avatar(
        cls: type[Self],
        avatar_id: UUID,
        content: bytes,
        size: int,
        extension: Extensions,
        unit_of_work: UnitOfWorkTracker,
    ) -> Self:
        avatar = cls(avatar_id, unit_of_work, content, FileData(extension, size), datetime.now(UTC))
        avatar.record_event[AvatarCreated](AvatarCreated(avatar_id, extension, avatar.created_at))

        return avatar

    def delete_avatar(self) -> None:
        self.mark_deleted()
        self.record_event[AvatarDeleted](AvatarDeleted(self.avatar_id))
