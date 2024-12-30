from dataclasses import dataclass
from uuid import UUID

from app.application.common.event_bus import EventBus
from app.application.common.unit_of_work import UnitOfWork
from app.domain.model.user.exceptions.user_exceptions import UserNotFoundError
from app.domain.model.user.repositories.user_repository import UserRepository


@dataclass(frozen=True)
class ChangeAddressCommand:
    user_id: UUID
    city: str | None
    country: str | None


class ChangeAddress:
    def __init__(self, unit_of_work: UnitOfWork, repository: UserRepository, event_bus: EventBus) -> None:
        self.unit_of_work = unit_of_work
        self.repository = repository
        self.event_bus = event_bus

    async def execute(self, command: ChangeAddressCommand) -> None:
        user = await self.repository.with_id(uuid=command.user_id)

        if not user:
            raise UserNotFoundError(title=f"User with id: {command.user_id} does not exist")

        user.change_address(city=command.city, country=command.country)

        await self.event_bus.publish(events=user.raise_events())
        await self.unit_of_work.commit()
