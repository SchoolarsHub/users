from uuid import UUID

from app.application.common.identity_provider import IdentityProvider


class FakeIdentityProvider(IdentityProvider):
    def __init__(self, user_id: UUID | None = None) -> None:
        self.user_id = user_id

    async def get_current_user_id(self) -> UUID:
        return self.user_id

    async def set_current_user_id(self, user_id: UUID) -> None:
        self.user_id = user_id
