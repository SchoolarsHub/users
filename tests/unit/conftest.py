import pytest

from app.domain.model.linked_account.linked_account import LinkedAccount
from app.domain.model.user.user import User
from tests.mocks.database import FakeDatabase
from tests.mocks.event_bus import FakeEventBus
from tests.mocks.identity_provider import FakeIdentityProvider
from tests.mocks.registry import Registry
from tests.mocks.unit_of_work import FakeUnitOfWork
from tests.mocks.user_mappers import GenericDataMapper, LinkedAccountDataMapper, UserDataMapper
from tests.mocks.user_repository import FakeUserRepository


@pytest.fixture
def event_bus() -> FakeEventBus:
    return FakeEventBus()


@pytest.fixture
def database() -> FakeDatabase:
    return FakeDatabase()


@pytest.fixture
def identity_provider() -> FakeIdentityProvider:
    return FakeIdentityProvider()


@pytest.fixture
def user_datamapper(database: FakeDatabase) -> GenericDataMapper[User]:
    return UserDataMapper(database=database)


@pytest.fixture
def linked_account_datamapper(database: FakeDatabase) -> GenericDataMapper[LinkedAccount]:
    return LinkedAccountDataMapper(database=database)


@pytest.fixture
def registry(user_datamapper: GenericDataMapper[User], linked_account_datamapper: GenericDataMapper[LinkedAccount]) -> Registry:
    registry = Registry()
    registry.add_mapper(User, user_datamapper)
    registry.add_mapper(LinkedAccount, linked_account_datamapper)

    return registry


@pytest.fixture
def unit_of_work(registry: Registry) -> FakeUnitOfWork:
    return FakeUnitOfWork(registry=registry)


@pytest.fixture
def user_repository(unit_of_work: FakeUnitOfWork, database: FakeDatabase) -> FakeUserRepository:
    return FakeUserRepository(unit_of_work=unit_of_work, database=database)
