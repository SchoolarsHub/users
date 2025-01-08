from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from uuid import UUID

from app.domain.shared.event import Event


@dataclass(frozen=True)
class ExperienceCreated(Event):
    experience_id: UUID
    user_id: UUID
    specialization: str
    company_name: str
    description: str
    start_date: date = field(default_factory=lambda: datetime.now(tz=UTC).date())
    finish_date: date = field(default_factory=lambda: datetime.now(tz=UTC).date())


@dataclass(frozen=True)
class ExperienceSpecializationChanged(Event):
    experience_id: UUID
    user_id: UUID
    specialization: str


@dataclass(frozen=True)
class ExperienceCompanyNameChanged(Event):
    experience_id: UUID
    user_id: UUID
    company_name: str


@dataclass(frozen=True)
class ExperienceDescriptionChanged(Event):
    experience_id: UUID
    user_id: UUID
    description: str


@dataclass(frozen=True)
class ExperiencePeriodChanged(Event):
    experience_id: UUID
    user_id: UUID
    start_date: date = field(default_factory=lambda: datetime.now(tz=UTC).date())
    finish_date: date = field(default_factory=lambda: datetime.now(tz=UTC).date())


@dataclass(frozen=True)
class ExperienceDeleted(Event):
    experience_id: UUID
    user_id: UUID
