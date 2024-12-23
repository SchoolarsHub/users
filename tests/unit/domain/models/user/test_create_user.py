from uuid import uuid4

import pytest

from app.domain.models.user.entities.user import User
from app.domain.models.user.events.user_created import UserCreated
from app.domain.models.user.exceptions.user_exceptions import AddressValidationError, ContactsValidationError
from app.domain.models.user.value_objects.address import Address
from app.domain.models.user.value_objects.contacts import Contacts
from tests.mocks.unit_of_work import FakeUowTracker


def test_create_with_address(uow_tracker: FakeUowTracker) -> None:
    user = User.create_user(
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
    published_events = user.raise_events()

    assert user.contacts.email == "XXXXXXXXXXXXXXXXXX"
    assert user.contacts.phone_number == 0000000000000
    assert user.address.country == "Belarus"
    assert user.address.city == "Minsk"
    assert user.address.street == "Lenina"
    assert user.address.house_number == 1
    assert user.address.postal_code == 220000

    assert len(published_events) == 1
    assert isinstance(published_events[0], UserCreated)
    assert published_events[0].user_id == user.entity_id
    assert published_events[0].username == user.username
    assert published_events[0].contacts.phone_number == user.contacts.phone_number
    assert published_events[0].contacts.email == user.contacts.email
    assert published_events[0].address == user.address
    assert published_events[0].gender == user.gender

    assert uow_tracker.new.get(User) == user


def test_create_without_address(uow_tracker: FakeUowTracker) -> None:
    user = User.create_user(
        user_id=uuid4(),
        unit_of_work=uow_tracker,
        username="XXXXXXXX",
        contacts=Contacts(phone_number=0000000000000, email="XXXXXXXXXXXXXXXXXX"),
        gender="male",
    )
    published_events = user.raise_events()

    assert user.contacts.email == "XXXXXXXXXXXXXXXXXX"
    assert user.contacts.phone_number == 0000000000000
    assert user.address is None

    assert len(published_events) == 1
    assert isinstance(published_events[0], UserCreated)
    assert published_events[0].user_id == user.entity_id
    assert published_events[0].username == user.username
    assert published_events[0].contacts.phone_number == user.contacts.phone_number
    assert published_events[0].contacts.email == user.contacts.email
    assert published_events[0].address is None
    assert published_events[0].gender == user.gender

    assert uow_tracker.new.get(User) == user


def test_create_user_without_address(uow_tracker: FakeUowTracker) -> None:
    user = User.create_user(
        user_id=uuid4(),
        unit_of_work=uow_tracker,
        username="XXXXXXXX",
        contacts=Contacts(phone_number=0000000000000, email="XXXXXXXXXXXXXXXXXX"),
        gender="male",
    )

    published_events = user.raise_events()

    assert user.address is None
    assert user.contacts.email == "XXXXXXXXXXXXXXXXXX"
    assert user.contacts.phone_number == 0000000000000
    assert user.gender == "male"

    assert len(published_events) == 1
    assert isinstance(published_events[0], UserCreated)
    assert published_events[0].user_id == user.entity_id
    assert published_events[0].username == user.username
    assert published_events[0].contacts.phone_number == user.contacts.phone_number
    assert published_events[0].contacts.email == user.contacts.email
    assert published_events[0].address == user.address
    assert published_events[0].gender == user.gender

    assert uow_tracker.new.get(User) == user


def test_create_user_with_invalid_email(uow_tracker: FakeUowTracker) -> None:
    with pytest.raises(ContactsValidationError):
        User.create_user(
            user_id=uuid4(),
            unit_of_work=uow_tracker,
            username="XXXXXXXX",
            contacts=Contacts(phone_number=0000000000000, email=1),
            address=Address(
                country="Belarus",
                city="Minsk",
                street="Lenina",
                house_number=1,
                postal_code=220000,
            ),
            gender="male",
        )

    assert uow_tracker.dirty.get(User) is None


def test_create_user_with_invalid_phone_number(uow_tracker: FakeUowTracker) -> None:
    with pytest.raises(ContactsValidationError):
        User.create_user(
            user_id=uuid4(),
            unit_of_work=uow_tracker,
            username="XXXXXXXX",
            contacts=Contacts(phone_number="XXXXXXXXXXXXXXXXXX", email="XXXXXXXXXXXXXXXXXX"),
            address=Address(
                country="Belarus",
                city="Minsk",
                street="Lenina",
                house_number=1,
                postal_code=220000,
            ),
            gender="male",
        )

    assert uow_tracker.dirty.get(User) is None


def test_create_user_with_invalid_address(uow_tracker: FakeUowTracker) -> None:
    with pytest.raises(AddressValidationError):
        User.create_user(
            user_id=uuid4(),
            unit_of_work=uow_tracker,
            username="XXXXXXXX",
            contacts=Contacts(phone_number=0000000000000, email="XXXXXXXXXXXXXXXXXX"),
            address=Address(
                country="Belarus",
                city="Minsk",
                street="Lenina",
                house_number=1,
                postal_code="XXXXXXXXXXXXXXXXXX",
            ),
            gender="male",
        )

    assert uow_tracker.dirty.get(User) is None
