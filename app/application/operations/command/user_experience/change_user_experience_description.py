from dataclasses import dataclass
from uuid import UUID

from app.application.common.event_bus import EventBus
from app.application.common.unit_of_work import UnitOfWork
from app.domain.model.user.exceptions import UserNotFoundError
from app.domain.model.user.repository import UserRepository


@dataclass(frozen=True)
class ChangeUserExperienceDescriptionCommand:
    user_id: UUID
    experience_info_id: UUID
    description: str


class ChangeUserExperienceDescription:
    def __init__(self, repository: UserRepository, unit_of_work: UnitOfWork, event_bus: EventBus) -> None:
        self.repository = repository
        self.unit_of_work = unit_of_work
        self.event_bus = event_bus

    async def execute(self, command: ChangeUserExperienceDescriptionCommand) -> None:
        user = await self.repository.with_id(command.user_id)

        if not user:
            raise UserNotFoundError(message=f"User with id: {command.user_id} not found")

        user.change_experience_description(command.experience_info_id, command.description)

        await self.event_bus.publish(events=user.raise_events())
        await self.unit_of_work.commit()
