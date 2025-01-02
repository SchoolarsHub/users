from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.application.operations.command.change_contacts import ChangeContacts, ChangeContactsCommand
from app.domain.model.user.events import ContactsChanged
from app.domain.model.user.exceptions import InactiveUserError, UserAlreadyExistsError, UserNotFoundError, UserTemporarilyDeletedError
from app.domain.model.user.statuses import Statuses
from app.domain.model.user.user import User
from app.domain.model.user.value_objects import Contacts, Fullname
from tests.mocks.database import FakeDatabase
from tests.mocks.event_bus import FakeEventBus
from tests.mocks.identity_provider import FakeIdentityProvider
from tests.mocks.unit_of_work import FakeUnitOfWork
from tests.mocks.user_repository import FakeUserRepository


@pytest.mark.asyncio
async def test_change_contacts_success(
    event_bus: FakeEventBus,
    unit_of_work: FakeUnitOfWork,
    user_repository: FakeUserRepository,
    identity_provider: FakeIdentityProvider,
    database: FakeDatabase,
) -> None:
    command_handler = ChangeContacts(event_bus, user_repository, unit_of_work, identity_provider)

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

    command = ChangeContactsCommand(email=None, phone=123)

    await command_handler.execute(command)

    changed_contacts_user = await user_repository.with_id(user.user_id)

    assert changed_contacts_user is not None
    assert changed_contacts_user.contacts.phone == command.phone
    assert changed_contacts_user.contacts.email == command.email

    assert len(event_bus.events) == 1
    assert isinstance(event_bus.events[0], ContactsChanged)
    assert event_bus.events[0].user_id == user.user_id
    assert event_bus.events[0].email == command.email
    assert event_bus.events[0].phone == command.phone

    assert unit_of_work.committed is True


@pytest.mark.asyncio
async def test_change_contacts_for_existing_emil(
    event_bus: FakeEventBus,
    unit_of_work: FakeUnitOfWork,
    user_repository: FakeUserRepository,
    identity_provider: FakeIdentityProvider,
    database: FakeDatabase,
) -> None:
    command_handler = ChangeContacts(event_bus, user_repository, unit_of_work, identity_provider)

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

    command = ChangeContactsCommand(email=user.contacts.email, phone=123)

    with pytest.raises(UserAlreadyExistsError):
        await command_handler.execute(command)

    assert len(event_bus.events) == 0
    assert unit_of_work.committed is False


@pytest.mark.asyncio
async def test_change_contacts_for_existing_phone(
    event_bus: FakeEventBus,
    unit_of_work: FakeUnitOfWork,
    user_repository: FakeUserRepository,
    identity_provider: FakeIdentityProvider,
    database: FakeDatabase,
) -> None:
    command_handler = ChangeContacts(event_bus, user_repository, unit_of_work, identity_provider)

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

    command = ChangeContactsCommand(email=None, phone=user.contacts.phone)

    with pytest.raises(UserAlreadyExistsError):
        await command_handler.execute(command)

    assert len(event_bus.events) == 0
    assert unit_of_work.committed is False


@pytest.mark.asyncio
async def test_change_contacts_for_inactive_user(
    event_bus: FakeEventBus,
    unit_of_work: FakeUnitOfWork,
    user_repository: FakeUserRepository,
    identity_provider: FakeIdentityProvider,
    database: FakeDatabase,
) -> None:
    command_handler = ChangeContacts(event_bus, user_repository, unit_of_work, identity_provider)

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

    command = ChangeContactsCommand(email=None, phone=1)

    with pytest.raises(InactiveUserError):
        await command_handler.execute(command)

    assert len(event_bus.events) == 0
    assert unit_of_work.committed is False


@pytest.mark.asyncio
async def test_change_contacts_for_temporarily_deleted_user(
    event_bus: FakeEventBus,
    unit_of_work: FakeUnitOfWork,
    user_repository: FakeUserRepository,
    identity_provider: FakeIdentityProvider,
    database: FakeDatabase,
) -> None:
    command_handler = ChangeContacts(event_bus, user_repository, unit_of_work, identity_provider)

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

    command = ChangeContactsCommand(email=None, phone=1234)

    with pytest.raises(UserTemporarilyDeletedError):
        await command_handler.execute(command)

    assert len(event_bus.events) == 0
    assert unit_of_work.committed is False


@pytest.mark.asyncio
async def test_change_contacts_for_not_found_user(
    event_bus: FakeEventBus,
    unit_of_work: FakeUnitOfWork,
    user_repository: FakeUserRepository,
    identity_provider: FakeIdentityProvider,
) -> None:
    command_handler = ChangeContacts(event_bus, user_repository, unit_of_work, identity_provider)

    await identity_provider.set_current_user_id(user_id=uuid4())

    command = ChangeContactsCommand(email=None, phone=1234)

    with pytest.raises(UserNotFoundError):
        await command_handler.execute(command)

    assert len(event_bus.events) == 0
    assert unit_of_work.committed is False
