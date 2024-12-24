from dataclasses import dataclass
from uuid import UUID

from app.domain.common.event import Event
from app.domain.models.profile.enums.allowed_extensions import AllowedExtensions


@dataclass(frozen=True)
class AvatarAdded(Event):
    profile_id: UUID
    user_id: UUID
    avatar_id: UUID
    file_name: str
    file_size: int
    file_extension: AllowedExtensions
