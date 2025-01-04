from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.application.operations.command.recovery_user import RecoveryUser, RecoveryUserCommand
from app.domain.model.user.events import UserRecoveried
from app.domain.model.user.exceptions import InactiveUserError, UserAlreadyActiveError
from app.domain.model.user.statuses import Statuses
from app.domain.model.user.user import User
from app.domain.model.user.value_objects import Contacts, Fullname
from tests.mocks.database import FakeDatabase
from tests.mocks.event_bus import FakeEventBus
from tests.mocks.unit_of_work import FakeUnitOfWork
from tests.mocks.user_repository import FakeUserRepository


@pytest.mark.asyncio
async def test_recovery_user_success(
    user_repository: FakeUserRepository,
    unit_of_work: FakeUnitOfWork,
    event_bus: FakeEventBus,
    database: FakeDatabase,
) -> None:
    command_handler = RecoveryUser(event_bus, user_repository, unit_of_work)

    user = User(
        user_id=uuid4(),
        unit_of_work=unit_of_work,
        contacts=Contacts(phone=123456789, email="123456@gmail.com"),
        fullname=Fullname(firstname="Jhon", lastname="Doe", middlename="Doe"),
        status=Statuses.DELETED,
        created_at=datetime.now(UTC),
        linked_accounts=[],
        deleted_at=datetime.now(UTC),
    )
    database.users[user.user_id] = user

    command = RecoveryUserCommand(user_id=user.user_id)

    await command_handler.execute(command=command)

    recoveried_user = await user_repository.with_id(user.user_id)

    assert recoveried_user is not None
    assert recoveried_user.status == Statuses.ACTIVE
    assert recoveried_user.deleted_at is None

    assert len(event_bus.events) == 1
    assert isinstance(event_bus.events[0], UserRecoveried)
    assert event_bus.events[0].user_id == user.user_id
    assert unit_of_work.committed is True


@pytest.mark.asyncio
async def test_recovery_already_active_user(
    user_repository: FakeUserRepository,
    unit_of_work: FakeUnitOfWork,
    event_bus: FakeEventBus,
    database: FakeDatabase,
) -> None:
    command_handler = RecoveryUser(event_bus, user_repository, unit_of_work)

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

    command = RecoveryUserCommand(user_id=user.user_id)

    with pytest.raises(UserAlreadyActiveError):
        await command_handler.execute(command=command)

    recoveried_user = await user_repository.with_id(user.user_id)

    assert recoveried_user is not None
    assert recoveried_user.status == Statuses.ACTIVE
    assert recoveried_user.deleted_at is None

    assert len(event_bus.events) == 0
    assert unit_of_work.committed is False


@pytest.mark.asyncio
async def test_recovery_inactive_user(
    user_repository: FakeUserRepository,
    unit_of_work: FakeUnitOfWork,
    event_bus: FakeEventBus,
    database: FakeDatabase,
) -> None:
    command_handler = RecoveryUser(event_bus, user_repository, unit_of_work)

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

    command = RecoveryUserCommand(user_id=user.user_id)

    with pytest.raises(InactiveUserError):
        await command_handler.execute(command=command)

    recoveried_user = await user_repository.with_id(user.user_id)

    assert recoveried_user is not None
    assert recoveried_user.status == Statuses.INACTIVE
    assert recoveried_user.deleted_at is None

    assert len(event_bus.events) == 0
    assert unit_of_work.committed is False
