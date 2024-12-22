from uuid import uuid4

from app.domain.models.user.entities.user import User
from app.domain.models.user.events.user_deleted import UserDeleted
from app.domain.models.user.value_objects.address import Address
from app.domain.models.user.value_objects.contacts import Contacts
from tests.mocks.unit_of_work import FakeUowTracker


def test_delete_user(uow_tracker: FakeUowTracker[User]) -> None:
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
    user.delete_user()
    published_events = user.raise_events()

    assert len(published_events) == 1
    assert isinstance(published_events[0], UserDeleted)
    assert published_events[0].user_id == user.entity_id

    assert uow_tracker.deleted.get(User) == user
