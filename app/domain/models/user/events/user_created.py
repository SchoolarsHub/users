from dataclasses import dataclass, field
from datetime import date
from uuid import UUID

from app.domain.common.event import Event
from app.domain.models.user.value_objects.address import Address
from app.domain.models.user.value_objects.contacts import Contacts


@dataclass(frozen=True)
class UserCreated(Event):
    user_id: UUID
    username: str
    contacts: Contacts
    address: Address | None = field(default=None)
    gender: str | None = field(default=None)
    birth_date: date | None = field(default=None)
