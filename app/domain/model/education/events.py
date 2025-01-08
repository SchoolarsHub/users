from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from uuid import UUID

from app.domain.shared.event import Event


@dataclass(frozen=True)
class EducationCreated(Event):
    education_id: UUID
    user_id: UUID
    organization: str
    degree: str
    education_field: str
    grade: str | None = field(default=None)
    start_date: date = field(default_factory=lambda: datetime.now(tz=UTC).date())
    end_date: date = field(default_factory=lambda: datetime.now(tz=UTC).date())


@dataclass(frozen=True)
class EducationOrganizationChanged(Event):
    education_id: UUID
    user_id: UUID
    organization: str


@dataclass(frozen=True)
class EducationDegreeChanged(Event):
    education_id: UUID
    user_id: UUID
    degree: str


@dataclass(frozen=True)
class EducationFieldChanged(Event):
    education_id: UUID
    user_id: UUID
    education_field: str


@dataclass(frozen=True)
class EducationGradeChanged(Event):
    education_id: UUID
    user_id: UUID
    grade: str | None = field(default=None)


@dataclass(frozen=True)
class EducationPeriodChanged(Event):
    education_id: UUID
    user_id: UUID
    start_date: date = field(default_factory=lambda: datetime.now(tz=UTC).date())
    end_date: date = field(default_factory=lambda: datetime.now(tz=UTC).date())


@dataclass(frozen=True)
class EducationDeleted(Event):
    education_id: UUID
    user_id: UUID
