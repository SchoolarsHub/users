from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from app.domain.models.user.entities.user import User


class UserRepository(Protocol):
    @abstractmethod
    def load_with_id(self, user_id: UUID) -> User:
        raise NotImplementedError

    @abstractmethod
    def ensure_username_unique(self, username: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def ensure_email_unique(self, email: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def ensure_phone_number_unique(self, phone_number: str) -> User:
        raise NotImplementedError
