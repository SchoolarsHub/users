from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID

from app.domain.model.user.events import (
    ContactsChanged,
    FullnameChanged,
    UserActivated,
    UserCreated,
    UserPermanentlyDeleted,
    UserRecoveried,
    UserTemporarilyDeleted,
)
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

    @staticmethod
    def from_domain_event(event: UserCreated) -> "UserCreatedIntegration":
        return UserCreatedIntegration(
            user_id=event.user_id,
            firstname=event.firstname,
            lastname=event.lastname,
            middlename=event.middlename,
            status=event.status,
            event_uuid=event.event_uuid,
            event_occured_at=event.event_occured_at,
        )


@dataclass(frozen=True, kw_only=True)
class UserActivatedIntegration(IntegrationEvent):
    user_id: UUID
    event_name: str = field(default="UserActivated")
    status: Statuses = field(default=Statuses.ACTIVE)

    @staticmethod
    def from_domain_event(event: UserActivated) -> "UserActivatedIntegration":
        return UserActivatedIntegration(
            user_id=event.user_id, status=event.status, event_uuid=event.event_uuid, event_occured_at=event.event_occured_at
        )


@dataclass(frozen=True, kw_only=True)
class FullnameChangedIntegration(IntegrationEvent):
    user_id: UUID
    firstname: str
    lastname: str
    middlename: str | None
    event_name: str = field(default="FullnameChanged")

    @staticmethod
    def from_domain_event(event: FullnameChanged) -> "FullnameChangedIntegration":
        return FullnameChangedIntegration(
            user_id=event.user_id,
            firstname=event.firstname,
            lastname=event.lastname,
            middlename=event.middlename,
            event_uuid=event.event_uuid,
            event_occured_at=event.event_occured_at,
        )


@dataclass(frozen=True, kw_only=True)
class ContactsChangedIntegration(IntegrationEvent):
    user_id: UUID
    email: str | None
    phone: int | None
    event_name: str = field(default="ContactsChanged")

    @staticmethod
    def from_domain_event(event: ContactsChanged) -> "ContactsChangedIntegration":
        return ContactsChangedIntegration(
            user_id=event.user_id, email=event.email, phone=event.phone, event_uuid=event.event_uuid, event_occured_at=event.event_occured_at
        )


@dataclass(frozen=True, kw_only=True)
class UserTemporarilyDeletedIntegration(IntegrationEvent):
    user_id: UUID
    event_name: str = field(default="UserTemporarilyDeleted")
    status: Statuses = field(default=Statuses.DELETED)
    deleted_at: datetime = field(default=datetime.now(UTC))

    @staticmethod
    def from_domain_event(event: UserTemporarilyDeleted) -> "UserTemporarilyDeletedIntegration":
        return UserTemporarilyDeletedIntegration(
            user_id=event.user_id,
            status=event.status,
            deleted_at=event.deleted_at,
            event_uuid=event.event_uuid,
            event_occured_at=event.event_occured_at,
        )


@dataclass(frozen=True, kw_only=True)
class UserRecoveriedIntegration(IntegrationEvent):
    user_id: UUID
    event_name: str = field(default="UserRecoveried")
    status: Statuses = field(default=Statuses.INACTIVE)

    @staticmethod
    def from_domain_event(event: UserRecoveried) -> "UserRecoveriedIntegration":
        return UserRecoveriedIntegration(
            user_id=event.user_id, status=event.status, event_uuid=event.event_uuid, event_occured_at=event.event_occured_at
        )


@dataclass(frozen=True, kw_only=True)
class UserPermanentlyDeletedIntegration(IntegrationEvent):
    user_id: UUID
    event_name: str = field(default="UserPermanentlyDeleted")

    @staticmethod
    def from_domain_event(event: UserPermanentlyDeleted) -> "UserPermanentlyDeletedIntegration":
        return UserPermanentlyDeletedIntegration(user_id=event.user_id, event_uuid=event.event_uuid, event_occured_at=event.event_occured_at)
