from app.application.common.event_bus import EventBus
from app.application.common.identity_provider import IdentityProvider
from app.application.common.unit_of_work import UnitOfWork
from app.domain.model.user.repository import UserRepository


class DeleteUserPermanently:
    def __init__(self, repository: UserRepository, unit_of_work: UnitOfWork, identity_provider: IdentityProvider, event_bus: EventBus) -> None:
        self.repository = repository
        self.unit_of_work = unit_of_work
        self.identity_provider = identity_provider
        self.event_bus = event_bus

    async def execute(self) -> None:
        current_user_id = await self.identity_provider.get_current_user_id()

        user = await self.repository.with_id(current_user_id)

        user.delete_user_permanently()

        self.repository.delete(user)
        await self.event_bus.publish(events=user.raise_events())
        await self.unit_of_work.commit()
