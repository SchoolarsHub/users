from dataclasses import dataclass
from uuid import UUID

from app.application.common.event_bus import EventBus
from app.application.common.unit_of_work import UnitOfWork
from app.domain.model.user.exceptions import UserNotFoundError
from app.domain.model.user.repository import UserRepository


@dataclass(frozen=True)
class ChangeFullnameCommand:
    user_id: UUID
    firstname: str
    lastname: str
    middlename: str | None


class ChangeFullname:
    def __init__(self, event_bus: EventBus, repository: UserRepository, unit_of_work: UnitOfWork) -> None:
        self.event_bus = event_bus
        self.repository = repository
        self.unit_of_work = unit_of_work

    async def execute(self, command: ChangeFullnameCommand) -> None:
        user = await self.repository.with_id(command.user_id)

        if not user:
            raise UserNotFoundError(message="User not found")

        user.change_fullname(command.firstname, command.lastname, command.middlename)

        self.repository.update(user)
        await self.event_bus.publish(events=user.raise_events())
        await self.unit_of_work.commit()
