from dataclasses import dataclass
from uuid import UUID

from app.domain.shared.event import Event


@dataclass(frozen=True)
class BioChanged(Event):
    user_id: UUID
    new_bio: str
