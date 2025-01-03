from datetime import UTC, datetime
from uuid import UUID

from app.domain.model.linked_account.events import ConnectionReasonChanged, LinkedAccountCreated, LinkedAccountDeleted
from app.domain.model.linked_account.exceptions import (
    LinkedAccountAlreadyExistsError,
    LinkedAccountNotExistsError,
)
from app.domain.model.linked_account.linked_account import LinkedAccount
from app.domain.model.linked_account.social_networks import SocialNetworks
from app.domain.model.user.events import (
    ContactsChanged,
    FullnameChanged,
    UserActivated,
    UserPermanentlyDeleted,
    UserRecoveried,
    UserTemporarilyDeleted,
)
from app.domain.model.user.exceptions import InactiveUserError, UserAlreadyActiveError, UserTemporarilyDeletedError
from app.domain.model.user.statuses import Statuses
from app.domain.model.user.value_objects import Contacts, Fullname
from app.domain.shared.base_entity import BaseEntity
from app.domain.shared.event import Event
from app.domain.shared.unit_of_work import UnitOfWorkTracker


class User(BaseEntity[UUID]):
    def __init__(
        self,
        user_id: UUID,
        unit_of_work: UnitOfWorkTracker,
        fullname: Fullname,
        contacts: Contacts,
        status: Statuses,
        linked_accounts: list[LinkedAccount],
        created_at: datetime,
        deleted_at: datetime | None = None,
    ) -> None:
        super().__init__(user_id)

        self.unit_of_work = unit_of_work
        self.user_id = user_id
        self.fullname = fullname
        self.contacts = contacts
        self.status = status
        self.created_at = created_at
        self.deleted_at = deleted_at
        self.linked_accounts = linked_accounts

        self._events: list[Event] = []

    def record_event(self, event: Event) -> None:
        self._events.append(event)

    def raise_events(self) -> list[Event]:
        events = self._events.copy()
        self._events.clear()

        return events

    def link_social_network(self, linked_account_id: UUID, social_netw: SocialNetworks, conn_link: str, connected_for: str | None) -> None:
        if self.status == Statuses.DELETED:
            raise UserTemporarilyDeletedError(message=f"User with id: {self.user_id} is temporarily deleted")

        if self.status == Statuses.INACTIVE:
            raise InactiveUserError(message=f"User with id: {self.user_id} is inactive")

        for linked_account in self.linked_accounts:
            if linked_account.social_network == social_netw:
                raise LinkedAccountAlreadyExistsError(message=f"Linked account with connection link: {conn_link} already exists")

        linked_account = LinkedAccount.create_linked_account(
            linked_account_id, self.user_id, social_netw, conn_link, connected_for, self.unit_of_work
        )
        self.linked_accounts.append(linked_account)
        self.record_event(LinkedAccountCreated(linked_account_id, social_netw, connected_for))

    def unlink_social_network(self, linked_account_id: UUID) -> None:
        if self.status == Statuses.DELETED:
            raise UserTemporarilyDeletedError(message=f"User with id: {self.user_id} is temporarily deleted")

        if self.status == Statuses.INACTIVE:
            raise InactiveUserError(message=f"User with id: {self.user_id} is inactive")

        for linked_account in self.linked_accounts:
            if linked_account.linked_account_id == linked_account_id:
                linked_account.delete_linked_account()
                self.record_event(LinkedAccountDeleted(linked_account_id))
                return

        raise LinkedAccountNotExistsError(message=f"Linked account with id: {linked_account_id} not exists")

    def change_social_network_connection_reason(self, linked_account_id: UUID, new_reason: str | None) -> None:
        if self.status == Statuses.DELETED:
            raise UserTemporarilyDeletedError(message=f"User with id: {self.user_id} is temporarily deleted")

        if self.status == Statuses.INACTIVE:
            raise InactiveUserError(message=f"User with id: {self.user_id} is inactive")

        for linked_account in self.linked_accounts:
            if linked_account.linked_account_id == linked_account_id:
                linked_account.change_connection_reason(new_reason)
                self.record_event(ConnectionReasonChanged(linked_account_id, new_reason))
                return

        raise LinkedAccountNotExistsError(message=f"Linked account with id: {linked_account_id} not exists")

    def activate_user(self) -> None:
        if self.status == Statuses.ACTIVE:
            raise UserAlreadyActiveError(message=f"User with id: {self.user_id} already have active status")

        if self.status == Statuses.DELETED:
            raise UserTemporarilyDeletedError(message=f"User with id: {self.user_id} is temporarily deleted")

        self.status = Statuses.ACTIVE
        self.record_event(UserActivated(user_id=self.user_id, status=self.status))

    def change_fullname(self, firstname: str, lastname: str, middlename: str | None) -> None:
        if self.status == Statuses.DELETED:
            raise UserTemporarilyDeletedError(message=f"User with id: {self.user_id} is temporarily deleted")

        if self.status == Statuses.INACTIVE:
            raise InactiveUserError(message=f"User with id: {self.user_id} is inactive")

        self.fullname = Fullname(firstname, lastname, middlename)
        self.record_event(FullnameChanged(user_id=self.user_id, firstname=firstname, lastname=lastname, middlename=middlename))

    def change_contacts(self, email: str | None, phone: int | None) -> None:
        if self.status == Statuses.DELETED:
            raise UserTemporarilyDeletedError(message=f"User with id: {self.user_id} is temporarily deleted")

        if self.status == Statuses.INACTIVE:
            raise InactiveUserError(message=f"User with id: {self.user_id} is inactive")

        self.contacts = Contacts(email, phone)
        self.record_event(ContactsChanged(user_id=self.user_id, email=email, phone=phone))

    def delete_user_temporarily(self) -> None:
        if self.status == Statuses.DELETED:
            raise UserTemporarilyDeletedError(message=f"User with id: {self.user_id} already temporarily deleted")

        if self.status == Statuses.INACTIVE:
            raise InactiveUserError(message=f"User with id: {self.user_id} is inactive")

        self.status = Statuses.DELETED
        self.deleted_at = datetime.now(UTC)
        self.record_event(UserTemporarilyDeleted(user_id=self.user_id, deleted_at=self.deleted_at, status=self.status))

    def recovery_user(self) -> None:
        if self.status == Statuses.INACTIVE:
            raise InactiveUserError(message=f"User with id: {self.user_id} is inactive")

        if self.status == Statuses.ACTIVE:
            raise UserAlreadyActiveError(message=f"User with id: {self.user_id} already have active status")

        self.status = Statuses.ACTIVE
        self.deleted_at = None
        self.record_event(UserRecoveried(user_id=self.user_id, status=self.status))

    def delete_user_permanently(self) -> None:
        for linked_account in self.linked_accounts:
            linked_account.delete_linked_account()

        self.record_event(UserPermanentlyDeleted(user_id=self.user_id))
