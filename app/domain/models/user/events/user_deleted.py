from dataclasses import dataclass
from uuid import UUID

from app.domain.common.event import Event


@dataclass(frozen=True)
class UserDeleted(Event):
    user_id: UUID
