from dataclasses import dataclass
from uuid import UUID

from app.domain.common.event import Event


@dataclass(frozen=True)
class LinkedAccountDeleted(Event):
    profile_id: UUID
    user_id: UUID
    linked_account_id: UUID
