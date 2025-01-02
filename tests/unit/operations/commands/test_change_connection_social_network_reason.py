from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.application.operations.command.change_social_network_connection_reason import (
    ChangeSocialNetworkConnectionReason,
    ChangeSocialNetworkConnectionReasonCommand,
)
from app.domain.model.linked_account.events import ConnectionReasonChanged
from app.domain.model.linked_account.exceptions import LinkedAccountNotExistsError
from app.domain.model.linked_account.linked_account import LinkedAccount
from app.domain.model.linked_account.social_networks import SocialNetworks
from app.domain.model.user.exceptions import InactiveUserError, UserNotFoundError, UserTemporarilyDeletedError
from app.domain.model.user.statuses import Statuses
from app.domain.model.user.user import User
from app.domain.model.user.value_objects import Contacts, Fullname
from tests.mocks.database import FakeDatabase
from tests.mocks.event_bus import FakeEventBus
from tests.mocks.identity_provider import FakeIdentityProvider
from tests.mocks.unit_of_work import FakeUnitOfWork
from tests.mocks.user_repository import FakeUserRepository


@pytest.mark.asyncio
async def test_change_social_network_connection_reason_success(
    user_repository: FakeUserRepository,
    identity_provider: FakeIdentityProvider,
    unit_of_work: FakeUnitOfWork,
    event_bus: FakeEventBus,
    database: FakeDatabase,
) -> None:
    user_id = uuid4()
    command_handler = ChangeSocialNetworkConnectionReason(user_repository, event_bus, unit_of_work, identity_provider)

    user = User(
        user_id=user_id,
        unit_of_work=unit_of_work,
        contacts=Contacts(phone=123456789, email="123456@gmail.com"),
        fullname=Fullname(firstname="Jhon", lastname="Doe", middlename="Doe"),
        status=Statuses.ACTIVE,
        created_at=datetime.now(UTC),
        linked_accounts=[],
        deleted_at=None,
    )
    linked_account = LinkedAccount(
        linked_account_id=uuid4(),
        user_id=user_id,
        social_network=SocialNetworks.TELEGRAM,
        connection_link="telegram.com",
        unit_of_work=unit_of_work,
        connected_at=datetime.now(UTC),
        connected_for=None,
    )
    database.linked_accounts[linked_account.linked_account_id] = linked_account
    database.users[user.user_id] = user

    await identity_provider.set_current_user_id(user_id=user.user_id)

    command = ChangeSocialNetworkConnectionReasonCommand(linked_account_id=linked_account.linked_account_id, reason="busines")

    await command_handler.execute(command)
    user_with_changed_linked_account = await user_repository.with_id(user.user_id)

    assert user_with_changed_linked_account is not None
    assert len(user_with_changed_linked_account.linked_accounts) == 1
    linked_account = user_with_changed_linked_account.linked_accounts[0]

    assert linked_account.connected_for == command.reason
    assert linked_account.linked_account_id == command.linked_account_id
    assert linked_account.user_id == user_id

    assert len(event_bus.events) == 1
    assert isinstance(event_bus.events[0], ConnectionReasonChanged)
    assert event_bus.events[0].connected_for == command.reason

    assert unit_of_work.committed is True


@pytest.mark.asyncio
async def test_change_social_network_connection_reason_with_inactive_user(
    user_repository: FakeUserRepository,
    identity_provider: FakeIdentityProvider,
    unit_of_work: FakeUnitOfWork,
    event_bus: FakeEventBus,
    database: FakeDatabase,
) -> None:
    user_id = uuid4()
    command_handler = ChangeSocialNetworkConnectionReason(user_repository, event_bus, unit_of_work, identity_provider)

    user = User(
        user_id=user_id,
        unit_of_work=unit_of_work,
        contacts=Contacts(phone=123456789, email="123456@gmail.com"),
        fullname=Fullname(firstname="Jhon", lastname="Doe", middlename="Doe"),
        status=Statuses.INACTIVE,
        created_at=datetime.now(UTC),
        linked_accounts=[],
        deleted_at=None,
    )
    linked_account = LinkedAccount(
        linked_account_id=uuid4(),
        user_id=user_id,
        social_network=SocialNetworks.TELEGRAM,
        connection_link="telegram.com",
        unit_of_work=unit_of_work,
        connected_at=datetime.now(UTC),
        connected_for=None,
    )
    database.linked_accounts[linked_account.linked_account_id] = linked_account
    database.users[user.user_id] = user

    await identity_provider.set_current_user_id(user_id=user.user_id)

    command = ChangeSocialNetworkConnectionReasonCommand(linked_account_id=linked_account.linked_account_id, reason="busines")

    with pytest.raises(InactiveUserError):
        await command_handler.execute(command)

    assert len(event_bus.events) == 0
    assert unit_of_work.committed is False


@pytest.mark.asyncio
async def test_change_social_network_connection_reason_with_deleted_user(
    user_repository: FakeUserRepository,
    identity_provider: FakeIdentityProvider,
    unit_of_work: FakeUnitOfWork,
    event_bus: FakeEventBus,
    database: FakeDatabase,
) -> None:
    user_id = uuid4()
    command_handler = ChangeSocialNetworkConnectionReason(user_repository, event_bus, unit_of_work, identity_provider)

    user = User(
        user_id=user_id,
        unit_of_work=unit_of_work,
        contacts=Contacts(phone=123456789, email="123456@gmail.com"),
        fullname=Fullname(firstname="Jhon", lastname="Doe", middlename="Doe"),
        status=Statuses.DELETED,
        created_at=datetime.now(UTC),
        linked_accounts=[],
        deleted_at=None,
    )
    linked_account = LinkedAccount(
        linked_account_id=uuid4(),
        user_id=user_id,
        social_network=SocialNetworks.TELEGRAM,
        connection_link="telegram.com",
        unit_of_work=unit_of_work,
        connected_at=datetime.now(UTC),
        connected_for=None,
    )
    database.linked_accounts[linked_account.linked_account_id] = linked_account
    database.users[user.user_id] = user

    await identity_provider.set_current_user_id(user_id=user.user_id)

    command = ChangeSocialNetworkConnectionReasonCommand(linked_account_id=linked_account.linked_account_id, reason="busines")

    with pytest.raises(UserTemporarilyDeletedError):
        await command_handler.execute(command)

    assert len(event_bus.events) == 0
    assert unit_of_work.committed is False


@pytest.mark.asyncio
async def test_change_social_network_connection_reason_with_not_found_user(
    user_repository: FakeUserRepository,
    identity_provider: FakeIdentityProvider,
    unit_of_work: FakeUnitOfWork,
    event_bus: FakeEventBus,
    database: FakeDatabase,
) -> None:
    user_id = uuid4()
    command_handler = ChangeSocialNetworkConnectionReason(user_repository, event_bus, unit_of_work, identity_provider)

    user = User(
        user_id=user_id,
        unit_of_work=unit_of_work,
        contacts=Contacts(phone=123456789, email="123456@gmail.com"),
        fullname=Fullname(firstname="Jhon", lastname="Doe", middlename="Doe"),
        status=Statuses.DELETED,
        created_at=datetime.now(UTC),
        linked_accounts=[],
        deleted_at=None,
    )
    linked_account = LinkedAccount(
        linked_account_id=uuid4(),
        user_id=user_id,
        social_network=SocialNetworks.TELEGRAM,
        connection_link="telegram.com",
        unit_of_work=unit_of_work,
        connected_at=datetime.now(UTC),
        connected_for=None,
    )
    database.linked_accounts[linked_account.linked_account_id] = linked_account
    database.users[user.user_id] = user

    await identity_provider.set_current_user_id(user_id=uuid4())

    command = ChangeSocialNetworkConnectionReasonCommand(linked_account_id=linked_account.linked_account_id, reason="busines")

    with pytest.raises(UserNotFoundError):
        await command_handler.execute(command)

    assert len(event_bus.events) == 0
    assert unit_of_work.committed is False


@pytest.mark.asyncio
async def test_change_social_network_connection_reason_with_not_found_linked_account(
    user_repository: FakeUserRepository,
    identity_provider: FakeIdentityProvider,
    unit_of_work: FakeUnitOfWork,
    event_bus: FakeEventBus,
    database: FakeDatabase,
) -> None:
    user_id = uuid4()
    command_handler = ChangeSocialNetworkConnectionReason(user_repository, event_bus, unit_of_work, identity_provider)

    user = User(
        user_id=user_id,
        unit_of_work=unit_of_work,
        contacts=Contacts(phone=123456789, email="123456@gmail.com"),
        fullname=Fullname(firstname="Jhon", lastname="Doe", middlename="Doe"),
        status=Statuses.ACTIVE,
        created_at=datetime.now(UTC),
        linked_accounts=[],
        deleted_at=None,
    )
    linked_account = LinkedAccount(
        linked_account_id=uuid4(),
        user_id=user_id,
        social_network=SocialNetworks.TELEGRAM,
        connection_link="telegram.com",
        unit_of_work=unit_of_work,
        connected_at=datetime.now(UTC),
        connected_for=None,
    )
    database.linked_accounts[linked_account.linked_account_id] = linked_account
    database.users[user.user_id] = user

    await identity_provider.set_current_user_id(user_id=user_id)

    command = ChangeSocialNetworkConnectionReasonCommand(linked_account_id=uuid4(), reason="busines")

    with pytest.raises(LinkedAccountNotExistsError):
        await command_handler.execute(command)

    assert len(event_bus.events) == 0
    assert unit_of_work.committed is False
