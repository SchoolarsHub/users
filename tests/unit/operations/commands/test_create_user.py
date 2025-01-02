from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.application.operations.command.create_user import CreateUser, CreateUserCommand
from app.domain.model.user.events import UserCreated
from app.domain.model.user.exceptions import ContactsValidationError, UserAlreadyExistsError
from app.domain.model.user.statuses import Statuses
from app.domain.model.user.user import User
from app.domain.model.user.value_objects import Contacts, Fullname
from tests.mocks.event_bus import FakeEventBus
from tests.mocks.unit_of_work import FakeUnitOfWork
from tests.mocks.user_repository import FakeUserRepository


@pytest.mark.asyncio
async def test_create_user(
    event_bus: FakeEventBus,
    unit_of_work: FakeUnitOfWork,
    user_repository: FakeUserRepository,
) -> None:
    command_handler = CreateUser(event_bus, user_repository, unit_of_work)

    command = CreateUserCommand(
        phone=123456789,
        email="123456@gmail.com",
        firstname="Jhon",
        lastname="Doe",
        middlename="Doe",
    )

    user_id = await command_handler.execute(command=command)
    user = await user_repository.with_id(user_id)

    assert user.user_id == user_id
    assert user.deleted_at is None

    assert len(event_bus.events) == 1
    assert isinstance(event_bus.events[0], UserCreated)
    assert event_bus.events[0].user_id == user_id

    assert unit_of_work.committed is True


@pytest.mark.asyncio
async def test_create_user_with_not_existing_phone(
    event_bus: FakeEventBus, unit_of_work: FakeUnitOfWork, user_repository: FakeUserRepository
) -> None:
    command_handler = CreateUser(event_bus, user_repository, unit_of_work)

    command = CreateUserCommand(
        phone=None,
        email="1234567890@gmail.com",
        firstname="Jhon",
        lastname="Doe",
        middlename="Doe",
    )

    user_id = await command_handler.execute(command=command)
    user = await user_repository.with_id(user_id)

    assert user.user_id == user_id
    assert user.deleted_at is None
    assert user.contacts.phone is None

    assert len(event_bus.events) == 1
    assert isinstance(event_bus.events[0], UserCreated)
    assert event_bus.events[0].user_id == user_id

    assert unit_of_work.committed is True


@pytest.mark.asyncio
async def test_create_user_with_not_existing_email(
    event_bus: FakeEventBus, unit_of_work: FakeUnitOfWork, user_repository: FakeUserRepository
) -> None:
    command_handler = CreateUser(event_bus, user_repository, unit_of_work)

    command = CreateUserCommand(
        phone=12,
        email=None,
        firstname="Jhon",
        lastname="Doe",
        middlename="Doe",
    )

    user_id = await command_handler.execute(command=command)
    user = await user_repository.with_id(user_id)

    assert user.user_id == user_id
    assert user.deleted_at is None
    assert user.contacts.email is None

    assert len(event_bus.events) == 1
    assert isinstance(event_bus.events[0], UserCreated)
    assert event_bus.events[0].user_id == user_id

    assert unit_of_work.committed is True


@pytest.mark.asyncio
async def test_create_user_with_not_existing_phone_and_email(
    event_bus: FakeEventBus, unit_of_work: FakeUnitOfWork, user_repository: FakeUserRepository
) -> None:
    command_handler = CreateUser(event_bus, user_repository, unit_of_work)

    command = CreateUserCommand(
        phone=None,
        email=None,
        firstname="Jhon",
        lastname="Doe",
        middlename="Doe",
    )

    with pytest.raises(ContactsValidationError):
        await command_handler.execute(command=command)

    assert len(event_bus.events) == 0

    assert unit_of_work.committed is False


@pytest.mark.asyncio
async def test_create_user_with_existing_phone(event_bus: FakeEventBus, unit_of_work: FakeUnitOfWork, user_repository: FakeUserRepository) -> None:
    command_handler = CreateUser(event_bus, user_repository, unit_of_work)

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

    command = CreateUserCommand(
        phone=123456789,
        email=None,
        firstname="Jhon",
        lastname="Doe",
        middlename="Doe",
    )
    with pytest.raises(UserAlreadyExistsError):
        await command_handler.execute(command=command)

    assert len(event_bus.events) == 0


@pytest.mark.asyncio
async def test_create_user_with_existing_email(event_bus: FakeEventBus, unit_of_work: FakeUnitOfWork, user_repository: FakeUserRepository) -> None:
    command_handler = CreateUser(event_bus, user_repository, unit_of_work)

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

    command = CreateUserCommand(
        phone=None,
        email="123456@gmail.com",
        firstname="Jhon",
        lastname="Doe",
        middlename="Doe",
    )
    with pytest.raises(UserAlreadyExistsError):
        await command_handler.execute(command=command)

    assert len(event_bus.events) == 0
