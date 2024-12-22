import pytest

from tests.mocks.unit_of_work import FakeUowTracker


@pytest.fixture
def uow_tracker() -> FakeUowTracker:
    return FakeUowTracker()
