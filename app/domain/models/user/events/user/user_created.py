from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.models.user.enums.account_statuses import AccountStatuses
from app.domain.shared.event import Event


@dataclass(frozen=True)
class UserCreated(Event):
    user_id: UUID
    username: str
    email: str | None
    phone: int | None
    account_status: AccountStatuses
    bio: str | None
    city: str | None
    country: str | None
    created_at: datetime
