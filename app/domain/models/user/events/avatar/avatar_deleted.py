from dataclasses import dataclass
from uuid import UUID

from app.domain.shared.event import Event


@dataclass(frozen=True)
class AvatarDeleted(Event):
    user_id: UUID
    avatar_id: UUID
