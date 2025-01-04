from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID

from app.domain.model.user.statuses import Statuses
from app.infrastructure.event_bus.integration_events.integration_event import IntegrationEvent


@dataclass(frozen=True, kw_only=True)
class UserCreatedIntegration(IntegrationEvent):
    user_id: UUID
    firstname: str
    lastname: str
    middlename: str | None
    event_name: str = field(default="UserCreated")
    status: Statuses = field(default=Statuses.INACTIVE)


@dataclass(frozen=True, kw_only=True)
class UserActivatedIntegration(IntegrationEvent):
    user_id: UUID
    event_name: str = field(default="UserActivated")
    status: Statuses = field(default=Statuses.ACTIVE)


@dataclass(frozen=True, kw_only=True)
class FullnameChangedIntegration(IntegrationEvent):
    user_id: UUID
    firstname: str
    lastname: str
    middlename: str | None
    event_name: str = field(default="FullnameChanged")


@dataclass(frozen=True, kw_only=True)
class ContactsChangedIntegration(IntegrationEvent):
    user_id: UUID
    email: str | None
    phone: int | None
    event_name: str = field(default="ContactsChanged")


@dataclass(frozen=True, kw_only=True)
class UserTemporarilyDeletedIntegration(IntegrationEvent):
    user_id: UUID
    event_name: str = field(default="UserTemporarilyDeleted")
    status: Statuses = field(default=Statuses.DELETED)
    deleted_at: datetime = field(default=datetime.now(UTC))


@dataclass(frozen=True, kw_only=True)
class UserRecoveriedIntegration(IntegrationEvent):
    user_id: UUID
    event_name: str = field(default="UserRecoveried")
    status: Statuses = field(default=Statuses.INACTIVE)


@dataclass(frozen=True, kw_only=True)
class UserPermanentlyDeletedIntegration(IntegrationEvent):
    user_id: UUID
    event_name: str = field(default="UserPermanentlyDeleted")
