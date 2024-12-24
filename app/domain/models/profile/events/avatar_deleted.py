from dataclasses import dataclass
from uuid import UUID

from app.domain.common.event import Event


@dataclass(frozen=True)
class AvatarDeleted(Event):
    avatar_id: UUID
    profile_id: UUID
    user_id: UUID
