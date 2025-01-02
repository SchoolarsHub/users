from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.application.operations.command.change_fullname import ChangeFullname, ChangeFullnameCommand
from app.domain.model.user.events import FullnameChanged
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
async def test_change_fullname_success(
    event_bus: FakeEventBus,
    unit_of_work: FakeUnitOfWork,
    user_repository: FakeUserRepository,
    identity_provider: FakeIdentityProvider,
    database: FakeDatabase,
) -> None:
    command_handler = ChangeFullname(event_bus, user_repository, unit_of_work, identity_provider)

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

    command = ChangeFullnameCommand(firstname="Kall", lastname="Frix", middlename=None)

    await command_handler.execute(command)

    change_fullname_user = await user_repository.with_id(user.user_id)

    assert change_fullname_user is not None
    assert change_fullname_user.fullname.firstname == command.firstname
    assert change_fullname_user.fullname.lastname == command.lastname
    assert change_fullname_user.fullname.middlename == command.middlename

    assert len(event_bus.events) == 1
    assert isinstance(event_bus.events[0], FullnameChanged)
    assert event_bus.events[0].user_id == user.user_id
    assert event_bus.events[0].firstname == command.firstname
    assert event_bus.events[0].lastname == command.lastname
    assert event_bus.events[0].middlename == command.middlename

    assert unit_of_work.committed is True


@pytest.mark.asyncio
async def test_change_fullname_for_temporarily_deleted_user(
    event_bus: FakeEventBus,
    unit_of_work: FakeUnitOfWork,
    user_repository: FakeUserRepository,
    identity_provider: FakeIdentityProvider,
    database: FakeDatabase,
) -> None:
    command_handler = ChangeFullname(event_bus, user_repository, unit_of_work, identity_provider)

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

    command = ChangeFullnameCommand(firstname="Kall", lastname="Frix", middlename=None)

    with pytest.raises(UserTemporarilyDeletedError):
        await command_handler.execute(command)

    assert len(event_bus.events) == 0
    assert unit_of_work.committed is False


@pytest.mark.asyncio
async def test_change_fullname_for_inactive_user(
    event_bus: FakeEventBus,
    unit_of_work: FakeUnitOfWork,
    user_repository: FakeUserRepository,
    identity_provider: FakeIdentityProvider,
    database: FakeDatabase,
) -> None:
    command_handler = ChangeFullname(event_bus, user_repository, unit_of_work, identity_provider)

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

    command = ChangeFullnameCommand(firstname="Kall", lastname="Frix", middlename=None)

    with pytest.raises(InactiveUserError):
        await command_handler.execute(command)

    assert len(event_bus.events) == 0
    assert unit_of_work.committed is False
