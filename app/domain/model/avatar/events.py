from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID

from app.domain.model.avatar.extensions import Extensions
from app.domain.shared.event import Event


@dataclass(frozen=True)
class AvatarCreated(Event):
    avatar_id: UUID
    extension: Extensions
    created_at: datetime = field(default=datetime.now(UTC))


@dataclass(frozen=True)
class AvatarDeleted(Event):
    avatar_id: UUID
