from dataclasses import dataclass
from uuid import UUID

from app.domain.models.user.enums.account_statuses import AccountStatuses
from app.domain.shared.event import Event


@dataclass(frozen=True)
class StatusChanged(Event):
    user_id: UUID
    new_status: AccountStatuses
