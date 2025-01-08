from dataclasses import dataclass
from datetime import date
from uuid import UUID

from app.application.common.event_bus import EventBus
from app.application.common.unit_of_work import UnitOfWork
from app.domain.model.user.exceptions import UserNotFoundError
from app.domain.model.user.repository import UserRepository


@dataclass(frozen=True)
class AddUserExperienceInfoCommand:
    user_id: UUID
    company_name: str
    start_working_date: date
    finish_working_date: date
    description: str
    specialization: str


class AddUserExperienceInfo:
    def __init__(self, repository: UserRepository, unit_of_work: UnitOfWork, event_bus: EventBus) -> None:
        self.repository = repository
        self.unit_of_work = unit_of_work
        self.event_bus = event_bus

    async def execute(self, command: AddUserExperienceInfoCommand) -> UUID:
        user = await self.repository.with_id(command.user_id)

        if not user:
            raise UserNotFoundError(message=f"User with id: {command.user_id} not found")

        experience_info_id = user.add_experience(
            command.specialization,
            command.company_name,
            command.start_working_date,
            command.finish_working_date,
            command.description,
        )

        await self.event_bus.publish(events=user.raise_events())
        await self.unit_of_work.commit()

        return experience_info_id
