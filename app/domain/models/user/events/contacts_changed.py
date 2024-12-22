from dataclasses import dataclass
from uuid import UUID

from app.domain.common.event import Event
from app.domain.models.user.value_objects.contacts import Contacts


@dataclass(frozen=True)
class ContactsChanged(Event):
    user_id: UUID
    contacts: Contacts
