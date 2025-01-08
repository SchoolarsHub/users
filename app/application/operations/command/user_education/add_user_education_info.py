from dataclasses import dataclass, field
from datetime import date
from uuid import UUID

from app.application.common.event_bus import EventBus
from app.application.common.unit_of_work import UnitOfWork
from app.domain.model.user.exceptions import UserNotFoundError
from app.domain.model.user.repository import UserRepository


@dataclass(frozen=True)
class AddUserEducationInfo:
    user_id: UUID
    organization: str
    degree: str
    education_field: str
    grade: str | None = field(default=None)
    start_date: date
    finish_date: date


class AddUserEducationInfoHandler:
    def __init__(self, repository: UserRepository, unit_of_work: UnitOfWork, event_bus: EventBus) -> None:
        self.repository = repository
        self.unit_of_work = unit_of_work
        self.event_bus = event_bus

    async def execute(self, command: AddUserEducationInfo) -> UUID:
        user = await self.repository.with_id(command.user_id)

        if not user:
            raise UserNotFoundError(message="User not found")

        education_id = user.add_education(
            command.organization,
            command.degree,
            command.education_field,
            command.grade,
            command.start_date,
            command.finish_date,
        )

        await self.event_bus.publish(events=user.raise_events())
        await self.unit_of_work.commit()

        return education_id
