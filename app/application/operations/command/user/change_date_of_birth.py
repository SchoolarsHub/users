from dataclasses import dataclass, field
from datetime import date
from uuid import UUID

from app.application.common.event_bus import EventBus
from app.application.common.unit_of_work import UnitOfWork
from app.domain.model.user.exceptions import UserNotFoundError
from app.domain.model.user.repository import UserRepository


@dataclass(frozen=True)
class ChangeDateOfBirthCommand:
    user_id: UUID
    date_of_birth: date | None = field(default=None)


class ChangeDateOfBirth:
    def __init__(self, repository: UserRepository, unit_of_work: UnitOfWork, event_bus: EventBus) -> None:
        self.repository = repository
        self.unit_of_work = unit_of_work
        self.event_bus = event_bus

    async def execute(self, command: ChangeDateOfBirthCommand) -> None:
        user = await self.repository.with_id(command.user_id)

        if not user:
            raise UserNotFoundError(message="User not found")

        user.change_date_of_birth(command.date_of_birth)

        await self.event_bus.publish(events=user.raise_events())
        await self.unit_of_work.commit()
