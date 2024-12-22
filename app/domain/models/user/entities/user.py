from datetime import date
from typing import Self
from uuid import UUID

from app.domain.common.event import Event
from app.domain.common.unit_of_work import UnitOfWorkTracker
from app.domain.common.uowed_entity import UowedEntity
from app.domain.models.user.events.contacts_changed import ContactsChanged
from app.domain.models.user.events.user_created import UserCreated
from app.domain.models.user.events.user_deleted import UserDeleted
from app.domain.models.user.value_objects.address import Address
from app.domain.models.user.value_objects.contacts import Contacts


class User(UowedEntity[UUID]):
    def __init__(
        self,
        user_id: UUID,
        username: str,
        unit_of_work: UnitOfWorkTracker[Self],
        contacts: Contacts,
        address: Address | None = None,
        gender: str | None = None,
        birt_date: date | None = None,
    ) -> None:
        super().__init__(user_id, unit_of_work)

        self._events: list[Event] = []
        self.username = username
        self.contacts = contacts
        self.address = address
        self.gender = gender
        self.birt_date = birt_date

    @classmethod
    def create_user(
        cls: type[Self],
        user_id: UUID,
        unit_of_work: UnitOfWorkTracker[Self],
        username: str,
        contacts: Contacts,
        address: Address | None = None,
        gender: str | None = None,
        birth_date: date | None = None,
    ) -> Self:
        user = cls(
            user_id=user_id,
            username=username,
            unit_of_work=unit_of_work,
            contacts=contacts,
            address=address,
            gender=gender,
            birth_date=birth_date,
        )

        user.add_event(
            UserCreated(
                user_id=user.entity_id,
                username=user.username,
                contacts=user.contacts,
                address=user.address,
                gender=user.gender,
                birth_date=user.birth_date,
                event_name="UserCreated",
                aggregate_name="User",
                aggregate_uuid=user.entity_id,
            )
        )
        user.mark_new()

        return user

    def change_username(self, username: str) -> None:
        self.username = username

    def change_contacts(self, contacts: Contacts) -> None:
        self.contacts = contacts
        self.add_event(
            ContactsChanged(
                user_id=self.entity_id,
                contacts=self.contacts,
                event_name="ContactsChanged",
                aggregate_name="User",
                aggregate_uuid=self.entity_id,
            )
        )

    def change_gender(self, gender: str) -> None:
        self.gender = gender

    def change_address(self, address: Address) -> None:
        self.address = address

    def change_birth_date(self, birth_date: date) -> None:
        self.birt_date = birth_date

    def delete_user(self) -> None:
        self.mark_deleted()
        self.add_event(
            UserDeleted(
                user_id=self.entity_id, event_name="UserDeleted", aggregate_name="User", aggregate_uuid=self.entity_id
            )
        )

    def add_event(self, event: Event) -> None:
        self._events.append(event)

    def raise_events(self) -> list[Event]:
        events = self._events.copy()
        self._events.clear()
        return events
