from dataclasses import dataclass
from uuid import UUID

from app.domain.shared.event import Event


@dataclass(frozen=True)
class ContactsChanged(Event):
    user_id: UUID
    new_email: str | None
    new_phone: int | None
