from abc import abstractmethod
from typing import Protocol

from app.infrastructure.brokers.message import Message


class MessagePublisher(Protocol):
    @abstractmethod
    async def publish(self, message: Message) -> None:
        raise NotImplementedError
