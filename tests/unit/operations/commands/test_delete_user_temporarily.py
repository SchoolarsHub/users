from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.application.operations.command.delete_user_temporarily import DeleteUserTemporarily
from app.domain.model.user.events import UserTemporarilyDeleted
from app.domain.model.user.exceptions import InactiveUserError, UserTemporarilyDeletedError
from app.domain.model.user.statuses import Statuses
from app.domain.model.user.user import User
from app.domain.model.user.value_objects import Contacts, Fullname
from tests.mocks.database import FakeDatabase
from tests.mocks.event_bus import FakeEventBus
from tests.mocks.identity_provider import FakeIdentityProvider
from tests.mocks.unit_of_work import FakeUnitOfWork
from tests.mocks.user_repository import FakeUserRepository


@pytest.mark.asyncio
async def test_delete_user_temporarily_success(
    user_repository: FakeUserRepository,
    identity_provider: FakeIdentityProvider,
    unit_of_work: FakeUnitOfWork,
    event_bus: FakeEventBus,
    database: FakeDatabase,
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
    database.users[user.user_id] = user
    await identity_provider.set_current_user_id(user_id=user.user_id)

    await command_handler.execute()
    deleted_user = await user_repository.with_id(user.user_id)

    assert deleted_user.status == Statuses.DELETED
    assert deleted_user.user_id == await identity_provider.get_current_user_id()
    assert deleted_user.deleted_at is not None

    assert len(event_bus.events) == 1
    assert isinstance(event_bus.events[0], UserTemporarilyDeleted)
    assert event_bus.events[0].user_id == user.user_id
    assert unit_of_work.committed is True


@pytest.mark.asyncio
async def test_delete_inactive_user_temporarily(
    user_repository: FakeUserRepository,
    identity_provider: FakeIdentityProvider,
    unit_of_work: FakeUnitOfWork,
    event_bus: FakeEventBus,
    database: FakeDatabase,
) -> None:
    command_handler = DeleteUserTemporarily(user_repository, unit_of_work, identity_provider, event_bus)

    user = User(
        user_id=uuid4(),
        unit_of_work=unit_of_work,
        contacts=Contacts(phone=123456789, email="123456@gmail.com"),
        fullname=Fullname(firstname="Jhon", lastname="Doe", middlename="Doe"),
        status=Statuses.INACTIVE,
        created_at=datetime.now(UTC),
        linked_accounts=[],
        deleted_at=None,
    )
    database.users[user.user_id] = user
    await identity_provider.set_current_user_id(user_id=user.user_id)

    with pytest.raises(InactiveUserError):
        await command_handler.execute()

    assert len(event_bus.events) == 0
    assert unit_of_work.committed is False


@pytest.mark.asyncio
async def test_delete_already_deleted_user_temporarily(
    user_repository: FakeUserRepository,
    identity_provider: FakeIdentityProvider,
    unit_of_work: FakeUnitOfWork,
    event_bus: FakeEventBus,
    database: FakeDatabase,
) -> None:
    command_handler = DeleteUserTemporarily(user_repository, unit_of_work, identity_provider, event_bus)

    user = User(
        user_id=uuid4(),
        unit_of_work=unit_of_work,
        contacts=Contacts(phone=123456789, email="123456@gmail.com"),
        fullname=Fullname(firstname="Jhon", lastname="Doe", middlename="Doe"),
        status=Statuses.DELETED,
        created_at=datetime.now(UTC),
        linked_accounts=[],
        deleted_at=None,
    )
    database.users[user.user_id] = user
    await identity_provider.set_current_user_id(user_id=user.user_id)

    with pytest.raises(UserTemporarilyDeletedError):
        await command_handler.execute()

    assert len(event_bus.events) == 0
    assert unit_of_work.committed is False
