from abc import abstractmethod
from typing import Protocol

from app.domain.shared.event import Event


class EventBus(Protocol):
    @abstractmethod
    async def publish(self, events: list[Event]) -> None:
        raise NotImplementedError
