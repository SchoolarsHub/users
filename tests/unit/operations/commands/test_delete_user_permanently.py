from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.application.operations.command.delete_user_permanently import DeleteUserPermanently
from app.domain.model.linked_account.linked_account import LinkedAccount
from app.domain.model.linked_account.social_networks import SocialNetworks
from app.domain.model.user.events import UserPermanentlyDeleted
from app.domain.model.user.exceptions import UserNotFoundError
from app.domain.model.user.statuses import Statuses
from app.domain.model.user.user import User
from app.domain.model.user.value_objects import Contacts, Fullname
from tests.mocks.database import FakeDatabase
from tests.mocks.event_bus import FakeEventBus
from tests.mocks.identity_provider import FakeIdentityProvider
from tests.mocks.unit_of_work import FakeUnitOfWork
from tests.mocks.user_repository import FakeUserRepository


@pytest.mark.asyncio
async def test_delete_user_permanently_success(
    user_repository: FakeUserRepository,
    identity_provider: FakeIdentityProvider,
    unit_of_work: FakeUnitOfWork,
    event_bus: FakeEventBus,
    database: FakeDatabase,
) -> None:
    command_handler = DeleteUserPermanently(user_repository, unit_of_work, identity_provider, event_bus)

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

    assert await user_repository.with_id(user.user_id) is None

    assert len(event_bus.events) == 1
    assert isinstance(event_bus.events[0], UserPermanentlyDeleted)
    assert event_bus.events[0].user_id == user.user_id

    assert unit_of_work.committed is True


@pytest.mark.asyncio
async def test_delete_user_permanently_with_linked_accounts(
    user_repository: FakeUserRepository,
    identity_provider: FakeIdentityProvider,
    unit_of_work: FakeUnitOfWork,
    event_bus: FakeEventBus,
    database: FakeDatabase,
) -> None:
    user_id = uuid4()
    command_handler = DeleteUserPermanently(user_repository, unit_of_work, identity_provider, event_bus)

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
    linked_accounts = [
        LinkedAccount(
            linked_account_id=uuid4(),
            user_id=user_id,
            social_network=SocialNetworks.TELEGRAM,
            connection_link="telegram.com",
            unit_of_work=unit_of_work,
            connected_at=datetime.now(UTC),
            connected_for=None,
        ),
        LinkedAccount(
            linked_account_id=uuid4(),
            user_id=user_id,
            social_network=SocialNetworks.TWITTER,
            connection_link="twitter.com",
            unit_of_work=unit_of_work,
            connected_at=datetime.now(UTC),
            connected_for=None,
        ),
    ]
    database.users[user.user_id] = user
    for account in linked_accounts:
        database.linked_accounts[account.linked_account_id] = account

    await identity_provider.set_current_user_id(user_id=user.user_id)

    await command_handler.execute()

    assert await user_repository.with_id(user.user_id) is None
    assert database.linked_accounts == {}

    assert len(event_bus.events) == 1
    assert isinstance(event_bus.events[0], UserPermanentlyDeleted)
    assert event_bus.events[0].user_id == user.user_id

    assert unit_of_work.committed is True


@pytest.mark.asyncio
async def test_delete_user_permanently_for_not_found_user(
    user_repository: FakeUserRepository, identity_provider: FakeIdentityProvider, unit_of_work: FakeUnitOfWork, event_bus: FakeEventBus
) -> None:
    command_handler = DeleteUserPermanently(user_repository, unit_of_work, identity_provider, event_bus)

    await identity_provider.set_current_user_id(user_id=uuid4())

    with pytest.raises(UserNotFoundError):
        await command_handler.execute()

    assert len(event_bus.events) == 0
    assert unit_of_work.committed is False
