from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from uuid import UUID

from app.domain.model.enums.specializations import Specializations
from app.domain.model.enums.statuses import Statuses
from app.domain.shared.event import Event


@dataclass(frozen=True)
class UserCreated(Event):
    user_id: UUID
    firstname: str
    lastname: str
    email: str
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


@dataclass(frozen=True)
class EmailChanged(Event):
    user_id: UUID
    email: str


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


@dataclass(frozen=True)
class BioChanged(Event):
    user_id: UUID
    bio: str | None = field(default=None)


@dataclass(frozen=True)
class DateOfBirthChanged(Event):
    user_id: UUID
    date_of_birth: date | None = field(default=None)


@dataclass(frozen=True)
class SpecializationChanged(Event):
    user_id: UUID
    specialization: Specializations | None = field(default=None)
