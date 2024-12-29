from dataclasses import dataclass
from uuid import UUID

from app.domain.shared.event import Event


@dataclass(frozen=True)
class AddressChanged(Event):
    user_id: UUID
    new_city: str | None
    new_country: str | None
