from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.application.operations.command.delete_user_temporarily import DeleteUserTemporarily
from app.domain.model.user.events import UserTemporarilyDeleted
from app.domain.model.user.statuses import Statuses
from app.domain.model.user.user import User
from app.domain.model.user.value_objects import Contacts, Fullname
from tests.mocks.event_bus import FakeEventBus
from tests.mocks.identity_provider import FakeIdentityProvider
from tests.mocks.unit_of_work import FakeUnitOfWork
from tests.mocks.user_repository import FakeUserRepository


@pytest.mark.asyncio
async def delete_user_temporarily_success(
    user_repository: FakeUserRepository, identity_provider: FakeIdentityProvider, unit_of_work: FakeUnitOfWork, event_bus: FakeEventBus
) -> None:
    command_handler = DeleteUserTemporarily(user_repository, unit_of_work, identity_provider, event_bus)

    user = User(
        user_id=uuid4(),
        unit_of_work=unit_of_work,
        contacts=Contacts(phone=123456789, email="123456@gmail.com"),
        fullname=Fullname(firstname="Jhon", lastname="Doe", middlename="Doe"),
        status=Statuses.ACTIVE,
        created_at=datetime.now(UTC),
        linked_accounts=[],
        deleted_at=None,
    )
    await user_repository.add(user)
    await unit_of_work.commit()
    await identity_provider.set_current_user_id(user_id=user.user_id)

    await command_handler.execute()
    deleted_user = await user_repository.with_id(user.user_id)

    assert deleted_user.status == Statuses.DELETED
    assert deleted_user.user_id == identity_provider.get_current_user_id()

    assert len(event_bus.events) == 1
    assert isinstance(event_bus.events[0], UserTemporarilyDeleted)
    assert event_bus.events[0].user_id == user.user_id
