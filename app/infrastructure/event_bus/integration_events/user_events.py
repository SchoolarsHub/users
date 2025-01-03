from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID

from app.domain.model.user.statuses import Statuses
from app.infrastructure.event_bus.integration_events.integration_event import IntegrationEvent


@dataclass(frozen=True)
class UserCreatedIntegration(IntegrationEvent):
    user_id: UUID
    firstname: str
    lastname: str
    middlename: str | None
    event_name: str = field(default="UserCreated")
    status: Statuses = field(default=Statuses.INACTIVE)


@dataclass(frozen=True)
class UserActivatedIntegration(IntegrationEvent):
    user_id: UUID
    event_name: str = field(default="UserActivated")
    status: Statuses = field(default=Statuses.ACTIVE)


@dataclass(frozen=True)
class FullnameChangedIntegration(IntegrationEvent):
    user_id: UUID
    firstname: str
    lastname: str
    event_name = field(default="FullnameChanged")
    middlename: str | None


@dataclass(frozen=True)
class ContactsChangedIntegration(IntegrationEvent):
    user_id: UUID
    email: str | None
    phone: int | None
    event_name = field(default="ContactsChanged")


@dataclass(frozen=True)
class UserTemporarilyDeletedIntegration(IntegrationEvent):
    user_id: UUID
    event_name: str = field(default="UserTemporarilyDeleted")
    status: Statuses = field(default=Statuses.DELETED)
    deleted_at: datetime = field(default=datetime.now(UTC))


@dataclass(frozen=True)
class UserRecoveriedIntegration(IntegrationEvent):
    user_id: UUID
    event_name: str = field(default="UserRecoveried")
    status: Statuses = field(default=Statuses.INACTIVE)


@dataclass(frozen=True)
class UserPermanentlyDeletedIntegration(IntegrationEvent):
    user_id: UUID
    event_name: str = field(default="UserPermanentlyDeleted")
