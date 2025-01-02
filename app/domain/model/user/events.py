from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID

from app.domain.model.user.statuses import Statuses
from app.domain.shared.event import Event


@dataclass(frozen=True)
class UserCreated(Event):
    user_id: UUID
    firstname: str
    lastname: str
    middlename: str | None
    status: Statuses = field(default=Statuses.INACTIVE)


@dataclass(frozen=True)
class UserActivated(Event):
    user_id: UUID
    status: Statuses = field(default=Statuses.ACTIVE)


@dataclass(frozen=True)
class FullnameChanged(Event):
    user_id: UUID
    firstname: str
    lastname: str
    middlename: str | None


@dataclass(frozen=True)
class ContactsChanged(Event):
    user_id: UUID
    email: str | None
    phone: int | None


@dataclass(frozen=True)
class UserTemporarilyDeleted(Event):
    user_id: UUID
    status: Statuses = field(default=Statuses.DELETED)
    deleted_at: datetime = field(default=datetime.now(UTC))


@dataclass(frozen=True)
class UserRecoveried(Event):
    user_id: UUID
    status: Statuses = field(default=Statuses.INACTIVE)


@dataclass(frozen=True)
class UserPermanentlyDeleted(Event):
    user_id: UUID
