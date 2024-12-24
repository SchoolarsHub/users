from dataclasses import dataclass
from uuid import UUID

from app.domain.common.event import Event
from app.domain.models.profile.enums.profile_types import ProfileTypes


@dataclass(frozen=True)
class ProfileCreated(Event):
    profile_id: UUID
    user_id: UUID
    profile_type: ProfileTypes
    first_name: str
    last_name: str
    middle_name: str | None
    bio: str | None
