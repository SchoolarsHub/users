from uuid import uuid4

import pytest

from app.domain.models.user.entities.user import User
from app.domain.models.user.exceptions.user_exceptions import AddressValidationError
from app.domain.models.user.value_objects.address import Address
from app.domain.models.user.value_objects.contacts import Contacts
from tests.mocks.unit_of_work import FakeUowTracker


def test_change_address(uow_tracker: FakeUowTracker[User]) -> None:
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
    new_address = Address(
        country="Russia",
        city="Petrozavodsk",
        street="Lenina",
        house_number=1,
        postal_code=127001,
    )
    user.change_address(new_address)

    assert user.address.city == new_address.city
    assert user.address.country == new_address.country
    assert user.address.house_number == new_address.house_number
    assert user.address.postal_code == new_address.postal_code
    assert user.address.street == new_address.street


def test_change_address_with_invalid_address(uow_tracker: FakeUowTracker[User]) -> None:
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
    with pytest.raises(AddressValidationError):
        user.change_address(
            Address(
                country=242,
                city=23,
                street=None,
                house_number="Jhon",
                postal_code=None,
            )
        )
