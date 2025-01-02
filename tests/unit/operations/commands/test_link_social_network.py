from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.application.operations.command.link_social_network import LinkSocialNetwork, LinkSocialNetworkCommand
from app.domain.model.linked_account.events import LinkedAccountCreated
from app.domain.model.linked_account.exceptions import ConnectionLinkNotBelongsToSocialNetworkError, LinkedAccountAlreadyExistsError
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
async def test_link_social_network(
    user_repository: FakeUserRepository,
    identity_provider: FakeIdentityProvider,
    unit_of_work: FakeUnitOfWork,
    event_bus: FakeEventBus,
    database: FakeDatabase,
) -> None:
    user_id = uuid4()
    command_handler = LinkSocialNetwork(event_bus, user_repository, unit_of_work, identity_provider)

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
    database.users[user.user_id] = user

    await identity_provider.set_current_user_id(user_id=user.user_id)

    command = LinkSocialNetworkCommand(social_network=SocialNetworks.TELEGRAM, connection_link="telegram.com", connected_for="busines")

    linked_account_id = await command_handler.execute(command)
    user_with_linked_account = await user_repository.with_id(user.user_id)

    assert user_with_linked_account is not None
    assert len(user.linked_accounts) == 1

    user_linked_account = user_with_linked_account.linked_accounts[0]

    assert user_linked_account.social_network == command.social_network
    assert user_linked_account.user_id == user.user_id
    assert user_linked_account.connection_link == command.connection_link
    assert user_linked_account.connected_for == command.connected_for
    assert user_linked_account.linked_account_id == linked_account_id

    assert len(event_bus.events) == 1
    assert isinstance(event_bus.events[0], LinkedAccountCreated)
    assert event_bus.events[0].connected_for == command.connected_for
    assert event_bus.events[0].social_network == command.social_network

    assert unit_of_work.committed is True


@pytest.mark.asyncio
async def test_link_social_network_for_inactive_user(
    user_repository: FakeUserRepository,
    identity_provider: FakeIdentityProvider,
    unit_of_work: FakeUnitOfWork,
    event_bus: FakeEventBus,
    database: FakeDatabase,
) -> None:
    user_id = uuid4()
    command_handler = LinkSocialNetwork(event_bus, user_repository, unit_of_work, identity_provider)

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
    database.users[user.user_id] = user

    await identity_provider.set_current_user_id(user_id=user.user_id)

    command = LinkSocialNetworkCommand(social_network=SocialNetworks.TELEGRAM, connection_link="telegram.com", connected_for="busines")

    with pytest.raises(InactiveUserError):
        await command_handler.execute(command)

    assert len(event_bus.events) == 0
    assert unit_of_work.committed is False


@pytest.mark.asyncio
async def test_link_social_network_for_deleted_user(
    user_repository: FakeUserRepository,
    identity_provider: FakeIdentityProvider,
    unit_of_work: FakeUnitOfWork,
    event_bus: FakeEventBus,
    database: FakeDatabase,
) -> None:
    user_id = uuid4()
    command_handler = LinkSocialNetwork(event_bus, user_repository, unit_of_work, identity_provider)

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
    database.users[user.user_id] = user

    await identity_provider.set_current_user_id(user_id=user.user_id)

    command = LinkSocialNetworkCommand(social_network=SocialNetworks.TELEGRAM, connection_link="telegram.com", connected_for="busines")

    with pytest.raises(UserTemporarilyDeletedError):
        await command_handler.execute(command)

    assert len(event_bus.events) == 0
    assert unit_of_work.committed is False


@pytest.mark.asyncio
async def test_link_social_network_for_not_found_user(
    user_repository: FakeUserRepository,
    identity_provider: FakeIdentityProvider,
    unit_of_work: FakeUnitOfWork,
    event_bus: FakeEventBus,
    database: FakeDatabase,
) -> None:
    user_id = uuid4()
    command_handler = LinkSocialNetwork(event_bus, user_repository, unit_of_work, identity_provider)

    await identity_provider.set_current_user_id(user_id=user_id)

    command = LinkSocialNetworkCommand(social_network=SocialNetworks.TELEGRAM, connection_link="telegram.com", connected_for="busines")

    with pytest.raises(UserNotFoundError):
        await command_handler.execute(command)

    assert len(event_bus.events) == 0
    assert unit_of_work.committed is False


@pytest.mark.asyncio
async def test_link_social_network_with_invalid_connection_link(
    user_repository: FakeUserRepository,
    identity_provider: FakeIdentityProvider,
    unit_of_work: FakeUnitOfWork,
    event_bus: FakeEventBus,
    database: FakeDatabase,
) -> None:
    user_id = uuid4()
    command_handler = LinkSocialNetwork(event_bus, user_repository, unit_of_work, identity_provider)

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
    database.users[user.user_id] = user

    await identity_provider.set_current_user_id(user_id=user.user_id)

    command = LinkSocialNetworkCommand(social_network=SocialNetworks.TELEGRAM, connection_link="twitter.com", connected_for="busines")

    with pytest.raises(ConnectionLinkNotBelongsToSocialNetworkError):
        await command_handler.execute(command)

    assert len(event_bus.events) == 0
    assert unit_of_work.committed is False


@pytest.mark.asyncio
async def test_link_social_network_to_user_with_already_exists_linked_account(
    user_repository: FakeUserRepository,
    identity_provider: FakeIdentityProvider,
    unit_of_work: FakeUnitOfWork,
    event_bus: FakeEventBus,
    database: FakeDatabase,
) -> None:
    user_id = uuid4()
    command_handler = LinkSocialNetwork(event_bus, user_repository, unit_of_work, identity_provider)

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

    command = LinkSocialNetworkCommand(social_network=SocialNetworks.TELEGRAM, connection_link="telegram.com", connected_for="busines")

    with pytest.raises(LinkedAccountAlreadyExistsError):
        await command_handler.execute(command)

    assert len(event_bus.events) == 0
    assert unit_of_work.committed is False
