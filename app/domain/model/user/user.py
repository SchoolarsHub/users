from datetime import UTC, datetime
from typing import Self
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
from app.domain.model.user.exceptions import InactiveUserError, UserAlreadyActiveError, UserTemporarilyDeletedError
from app.domain.model.user.statuses import Statuses
from app.domain.model.user.value_objects import Contacts, Fullname
from app.domain.shared.event import Event
from app.domain.shared.unit_of_work import UnitOfWorkTracker
from app.domain.shared.uowed_entity import UowedEntity


class User(UowedEntity[UUID]):
    def __init__(
        self,
        user_id: UUID,
        unit_of_work: UnitOfWorkTracker,
        fullname: Fullname,
        contacts: Contacts,
        status: Statuses,
        created_at: datetime,
        deleted_at: datetime | None = None,
    ) -> None:
        super().__init__(user_id, unit_of_work)

        self.user_id = user_id
        self.fullname = fullname
        self.contacts = contacts
        self.status = status
        self.created_at = created_at
        self.deleted_at = deleted_at

        self._events: list[Event] = []

    def record_event[TEvent: Event](self, event: TEvent) -> None:
        self._events.append(event)

    def raise_events(self) -> list[Event]:
        events = self._events.copy()
        self._events.clear()

        return events

    @classmethod
    def create_user(
        cls: type[Self],
        user_id: UUID,
        firstname: str,
        lastname: str,
        middlename: str | None,
        email: str | None,
        phone: int | None,
        unit_of_work: UnitOfWorkTracker,
    ) -> None:
        user = cls(
            user_id,
            unit_of_work,
            Fullname(firstname, lastname, middlename),
            Contacts(email, phone),
            Statuses.INACTIVE,
            datetime.now(UTC),
        )
        user.mark_new()
        user.record_event[UserCreated](UserCreated(user_id=user_id, firstname=firstname, lastname=lastname, middlename=middlename))

        return user

    def activate_user(self) -> None:
        if self.status == Statuses.ACTIVE:
            raise UserAlreadyActiveError(title=f"User with id: {self.user_id} already have active status")

        if self.status == Statuses.DELETED:
            raise UserTemporarilyDeletedError(title=f"User with id: {self.user_id} is temporarily deleted")

        self.status = Statuses.ACTIVE
        self.mark_dirty()
        self.record_event[UserActivated](UserActivated(user_id=self.user_id, status=self.status))

    def change_fullname(self, firstname: str, lastname: str, middlename: str | None) -> None:
        if self.status == Statuses.DELETED:
            raise UserTemporarilyDeletedError(title=f"User with id: {self.user_id} is temporarily deleted")

        if self.status == Statuses.INACTIVE:
            raise InactiveUserError(title=f"User with id: {self.user_id} is inactive")

        self.fullname = Fullname(firstname, lastname, middlename)
        self.mark_dirty()
        self.record_event[FullnameChanged](FullnameChanged(user_id=self.user_id, firstname=firstname, lastname=lastname, middlename=middlename))

    def change_contacts(self, email: str | None, phone: int | None) -> None:
        if self.status == Statuses.DELETED:
            raise UserTemporarilyDeletedError(title=f"User with id: {self.user_id} is temporarily deleted")

        if self.status == Statuses.INACTIVE:
            raise InactiveUserError(title=f"User with id: {self.user_id} is inactive")

        self.contacts = Contacts(email, phone)
        self.mark_dirty()
        self.record_event[ContactsChanged](ContactsChanged(user_id=self.user_id, email=email, phone=phone))

    def delete_user_temporarily(self) -> None:
        if self.status == Statuses.DELETED:
            raise UserTemporarilyDeletedError(title=f"User with id: {self.user_id} already temporarily deleted")

        self.status = Statuses.DELETED
        self.deleted_at = datetime.now(UTC)
        self.mark_dirty()
        self.record_event[UserTemporarilyDeleted](UserTemporarilyDeleted(user_id=self.user_id, deleted_at=self.deleted_at, status=self.status))

    def recovery_user(self) -> None:
        if self.status != Statuses.DELETED:
            raise UserTemporarilyDeletedError(title=f"User with id: {self.user_id} is not temporarily deleted")

        self.status = Statuses.INACTIVE
        self.deleted_at = None
        self.mark_dirty()
        self.record_event[UserRecoveried](UserRecoveried(user_id=self.user_id, status=self.status))

    def delete_user_permanently(self) -> None:
        self.mark_deleted()
        self.record_event[UserPermanentlyDeleted](UserPermanentlyDeleted(user_id=self.user_id))
