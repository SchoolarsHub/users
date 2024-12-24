from dataclasses import dataclass
from uuid import UUID

from app.domain.common.event import Event
from app.domain.models.profile.enums.allowed_accounts import AllowedAccounts


@dataclass(frozen=True)
class LinkedAccountAdded(Event):
    profile_id: UUID
    user_id: UUID
    linked_account_id: UUID
    linked_account_name: AllowedAccounts
    linked_account_url: str
