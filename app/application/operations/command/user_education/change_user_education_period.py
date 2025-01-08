from dataclasses import dataclass
from datetime import date
from uuid import UUID

from app.application.common.event_bus import EventBus
from app.application.common.unit_of_work import UnitOfWork
from app.domain.model.user.exceptions import UserNotFoundError
from app.domain.model.user.repository import UserRepository


@dataclass(frozen=True)
class ChangeUserEducationPeriodCommand:
    user_id: UUID
    education_id: UUID
    start_education_date: date
    finish_education_date: date


class ChangeUserEducationPeriod:
    def __init__(self, repository: UserRepository, unit_of_work: UnitOfWork, event_bus: EventBus) -> None:
        self.repository = repository
        self.unit_of_work = unit_of_work
        self.event_bus = event_bus

    async def execute(self, command: ChangeUserEducationPeriodCommand) -> None:
        user = await self.repository.with_id(command.user_id)

        if not user:
            raise UserNotFoundError(message=f"User with id: {command.user_id} not found")

        user.change_education_period(command.education_id, command.start_education_date, command.finish_education_date)

        await self.event_bus.publish(events=user.raise_events())
        await self.unit_of_work.commit()
