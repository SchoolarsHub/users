from dataclasses import dataclass
from uuid import UUID

from app.domain.shared.event import Event


@dataclass(frozen=True)
class SocialNetworkUnlinked(Event):
    user_id: UUID
    linked_account_id: UUID
