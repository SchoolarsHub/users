from datetime import UTC, datetime
from typing import Self
from uuid import UUID

from app.domain.model.avatar.events import AvatarCreated, AvatarDeleted
from app.domain.model.avatar.extensions import Extensions
from app.domain.model.avatar.value_objects import FileData
from app.domain.shared.base_entity import BaseEntity
from app.domain.shared.event import Event


class Avatar(BaseEntity[UUID]):
    def __init__(
        self,
        avatar_id: UUID,
        content: bytes,
        file_data: FileData,
        created_at: datetime,
    ) -> None:
        super().__init__(avatar_id)

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
    ) -> Self:
        avatar = cls(avatar_id, content, FileData(extension, size), datetime.now(UTC))
        avatar.record_event[AvatarCreated](AvatarCreated(avatar_id, extension, avatar.created_at))

        return avatar

    def delete_avatar(self) -> None:
        self.record_event[AvatarDeleted](AvatarDeleted(self.avatar_id))
