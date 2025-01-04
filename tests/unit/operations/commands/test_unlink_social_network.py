from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.application.operations.command.unlink_social_network import UnlinkSocialNetwork, UnlinkSocialNetworkCommand
from app.domain.model.linked_account.events import LinkedAccountDeleted
from app.domain.model.linked_account.exceptions import LinkedAccountNotExistsError
from app.domain.model.linked_account.linked_account import LinkedAccount
from app.domain.model.linked_account.social_networks import SocialNetworks
from app.domain.model.user.exceptions import InactiveUserError, UserTemporarilyDeletedError
from app.domain.model.user.statuses import Statuses
from app.domain.model.user.user import User
from app.domain.model.user.value_objects import Contacts, Fullname
from tests.mocks.database import FakeDatabase
from tests.mocks.event_bus import FakeEventBus
from tests.mocks.unit_of_work import FakeUnitOfWork
from tests.mocks.user_repository import FakeUserRepository


@pytest.mark.asyncio
async def test_unlink_social_network_success(
    user_repository: FakeUserRepository,
    unit_of_work: FakeUnitOfWork,
    event_bus: FakeEventBus,
    database: FakeDatabase,
) -> None:
    user_id = uuid4()
    command_handler = UnlinkSocialNetwork(event_bus, user_repository, unit_of_work)

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

    command = UnlinkSocialNetworkCommand(
        user_id=user_id,
        linked_account_id=linked_account.linked_account_id,
    )

    await command_handler.execute(command)

    user = await user_repository.with_id(user_id)

    assert len(user.linked_accounts) == 0
    assert len(event_bus.events) == 1
    assert isinstance(event_bus.events[0], LinkedAccountDeleted)
    assert event_bus.events[0].linked_account_id == command.linked_account_id

    assert unit_of_work.committed is True


@pytest.mark.asyncio
async def test_unlink_social_network_for_inactive_user(
    user_repository: FakeUserRepository,
    unit_of_work: FakeUnitOfWork,
    event_bus: FakeEventBus,
    database: FakeDatabase,
) -> None:
    user_id = uuid4()
    command_handler = UnlinkSocialNetwork(event_bus, user_repository, unit_of_work)

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

    command = UnlinkSocialNetworkCommand(
        user_id=user_id,
        linked_account_id=linked_account.linked_account_id,
    )

    with pytest.raises(InactiveUserError):
        await command_handler.execute(command)

    user = await user_repository.with_id(user_id)

    assert len(user.linked_accounts) == 1
    assert len(event_bus.events) == 0
    assert unit_of_work.committed is False


@pytest.mark.asyncio
async def test_unlink_social_network_for_deleted_user(
    user_repository: FakeUserRepository,
    unit_of_work: FakeUnitOfWork,
    event_bus: FakeEventBus,
    database: FakeDatabase,
) -> None:
    user_id = uuid4()
    command_handler = UnlinkSocialNetwork(event_bus, user_repository, unit_of_work)

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

    command = UnlinkSocialNetworkCommand(
        user_id=user_id,
        linked_account_id=linked_account.linked_account_id,
    )

    with pytest.raises(UserTemporarilyDeletedError):
        await command_handler.execute(command)

    user = await user_repository.with_id(user_id)

    assert len(user.linked_accounts) == 1
    assert len(event_bus.events) == 0
    assert unit_of_work.committed is False


@pytest.mark.asyncio
async def test_unlink_not_exists_social_network(
    user_repository: FakeUserRepository,
    unit_of_work: FakeUnitOfWork,
    event_bus: FakeEventBus,
    database: FakeDatabase,
) -> None:
    user_id = uuid4()
    command_handler = UnlinkSocialNetwork(event_bus, user_repository, unit_of_work)

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

    command = UnlinkSocialNetworkCommand(user_id=user_id, linked_account_id=uuid4())

    with pytest.raises(LinkedAccountNotExistsError):
        await command_handler.execute(command)

    user = await user_repository.with_id(user_id)

    assert len(user.linked_accounts) == 1
    assert len(event_bus.events) == 0
    assert unit_of_work.committed is False
