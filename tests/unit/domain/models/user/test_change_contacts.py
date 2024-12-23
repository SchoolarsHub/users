from uuid import uuid4

import pytest

from app.domain.models.user.entities.user import User
from app.domain.models.user.events.contacts_changed import ContactsChanged
from app.domain.models.user.exceptions.user_exceptions import ContactsValidationError
from app.domain.models.user.value_objects.address import Address
from app.domain.models.user.value_objects.contacts import Contacts
from tests.mocks.unit_of_work import FakeUowTracker


def test_change_user_contacts(uow_tracker: FakeUowTracker) -> None:
    user = User(
        user_id=uuid4(),
        unit_of_work=uow_tracker,
        username="flixxiss",
        contacts=Contacts(phone_number=0000000000000, email="XXXXXXXXXXXXXXXXXX"),
        address=Address(
            country="Belarus",
            city="Minsk",
            street="Lenina",
            house_number=1,
            postal_code=220000,
        ),
        gender="male",
    )
    new_contacts = Contacts(phone_number=1111111111111, email="XXXXXXXXXXXXXXXXXX")
    user.change_contacts(contacts=new_contacts)
    published_events = user.raise_events()

    assert user.contacts.email == new_contacts.email
    assert user.contacts.phone_number == new_contacts.phone_number

    assert len(published_events) == 1
    assert isinstance(published_events[0], ContactsChanged)
    assert published_events[0].user_id == user.entity_id
    assert published_events[0].contacts.phone_number == user.contacts.phone_number
    assert published_events[0].contacts.email == user.contacts.email

    assert uow_tracker.dirty.get(User) == user


def test_change_contacts_with_null_email(uow_tracker: FakeUowTracker) -> None:
    user = User(
        user_id=uuid4(),
        unit_of_work=uow_tracker,
        username="XXXXXXXX",
        contacts=Contacts(phone_number=0000000000000, email="XXXXXXXXXXXXXXXXXX"),
        address=Address(
            country="Belarus",
            city="Minsk",
            street="Lenina",
            house_number=1,
            postal_code=220000,
        ),
        gender="male",
    )
    new_contacts = Contacts(phone_number=1111111111111, email=None)
    user.change_contacts(contacts=new_contacts)
    published_events = user.raise_events()

    assert user.contacts.email == new_contacts.email
    assert user.contacts.phone_number == new_contacts.phone_number

    assert len(published_events) == 1
    assert isinstance(published_events[0], ContactsChanged)
    assert published_events[0].user_id == user.entity_id
    assert published_events[0].contacts.phone_number == user.contacts.phone_number
    assert published_events[0].contacts.email == user.contacts.email

    assert uow_tracker.dirty.get(User) == user


def test_change_contacts_with_null_phone_number(uow_tracker: FakeUowTracker) -> None:
    user = User(
        user_id=uuid4(),
        unit_of_work=uow_tracker,
        username="XXXXXXXX",
        contacts=Contacts(phone_number=0000000000000, email="XXXXXXXXXXXXXXXXXX"),
        address=Address(
            country="Belarus",
            city="Minsk",
            street="Lenina",
            house_number=1,
            postal_code=220000,
        ),
        gender="male",
    )
    new_contacts = Contacts(phone_number=None, email="XXXXXXXXXXXXXXXXXX")
    user.change_contacts(contacts=new_contacts)
    published_events = user.raise_events()

    assert user.contacts.email == new_contacts.email
    assert user.contacts.phone_number == new_contacts.phone_number

    assert len(published_events) == 1
    assert isinstance(published_events[0], ContactsChanged)
    assert published_events[0].user_id == user.entity_id
    assert published_events[0].contacts.phone_number == user.contacts.phone_number
    assert published_events[0].contacts.email == user.contacts.email

    assert uow_tracker.dirty.get(User) == user


def test_change_contacts_with_invalid_email(uow_tracker: FakeUowTracker) -> None:
    user = User(
        user_id=uuid4(),
        unit_of_work=uow_tracker,
        username="flixxiss",
        contacts=Contacts(phone_number=0000000000000, email="XXXXXXXXXXXXXXXXXX"),
        address=Address(
            country="Belarus",
            city="Minsk",
            street="Lenina",
            house_number=1,
            postal_code=220000,
        ),
        gender="male",
    )
    with pytest.raises(ContactsValidationError):
        user.change_contacts(Contacts(phone_number=None, email=2))

    assert uow_tracker.dirty.get(User) is None


def test_change_contacts_with_invalid_phone_number(uow_tracker: FakeUowTracker) -> None:
    user = User(
        user_id=uuid4(),
        unit_of_work=uow_tracker,
        username="XXXXXXXX",
        contacts=Contacts(phone_number=0000000000000, email="XXXXXXXXXXXXXXXXXX"),
        address=Address(
            country="Belarus",
            city="Minsk",
            street="Lenina",
            house_number=1,
            postal_code=220000,
        ),
        gender="male",
    )
    with pytest.raises(ContactsValidationError):
        user.change_contacts(Contacts(phone_number="2", email="XXXXXXXXXXXXXXXXXX"))

    assert uow_tracker.dirty.get(User) is None


def test_change_user_contacts_with_null_email_and_phone(uow_tracker: FakeUowTracker) -> None:
    user = User(
        user_id=uuid4(),
        unit_of_work=uow_tracker,
        username="XXXXXXXX",
        contacts=Contacts(phone_number=0000000000000, email="XXXXXXXXXXXXXXXXXX"),
        address=Address(
            country="Belarus",
            city="Minsk",
            street="Lenina",
            house_number=1,
            postal_code=220000,
        ),
        gender="male",
    )
    with pytest.raises(ContactsValidationError):
        user.change_contacts(Contacts(phone_number=None, email=None))

    assert uow_tracker.dirty.get(User) is None
