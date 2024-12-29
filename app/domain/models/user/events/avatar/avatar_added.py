from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.shared.event import Event


@dataclass(frozen=True)
class AvatarAdded(Event):
    user_id: UUID
    avatar_id: UUID
    filename: str
    file_extension: str
    file_size: int
    uploaded_at: datetime
