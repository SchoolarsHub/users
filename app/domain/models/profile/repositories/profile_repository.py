from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from app.domain.models.profile.entities.profile import Profile


class ProfileRepository(Protocol):
    @abstractmethod
    async def load_profile_by_uuid(self, profile_id: UUID) -> Profile | None:
        raise NotImplementedError

    @abstractmethod
    async def load_profiles_by_user_id(self, user_id: UUID) -> list[Profile]:
        raise NotImplementedError
