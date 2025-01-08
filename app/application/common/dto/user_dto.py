from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.model.user.enums import Statuses


@dataclass(frozen=True)
class UserDTO:
    user_id: UUID
    status: Statuses
    created_at: datetime
    firstname: str
    lastname: str
