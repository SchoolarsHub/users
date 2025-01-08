from dataclasses import dataclass
from uuid import UUID

from app.application.common.event_bus import EventBus
from app.application.common.unit_of_work import UnitOfWork
from app.domain.model.user.exceptions import UserNotFoundError
from app.domain.model.user.repository import UserRepository


@dataclass(frozen=True)
class ChangeUserEducationFieldCommand:
    user_id: UUID
    education_id: UUID
    education_field: str


class ChangeUserEducationField:
    def __init__(self, repository: UserRepository, uow: UnitOfWork, event_bus: EventBus) -> None:
        self.repository = repository
        self.uow = uow
        self.event_bus = event_bus

    async def execute(self, command: ChangeUserEducationFieldCommand) -> None:
        user = await self.repository.with_id(command.user_id)

        if not user:
            raise UserNotFoundError(message=f"User with id: {command.user_id} not found")

        user.change_education_field(command.education_id, command.education_field)

        await self.event_bus.publish(events=user.raise_events())
        await self.uow.commit()
