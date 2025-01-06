from dataclasses import dataclass
from uuid import UUID

from app.application.common.event_bus import EventBus
from app.application.common.unit_of_work import UnitOfWork
from app.domain.model.user.exceptions import UserAlreadyExistsError, UserNotFoundError
from app.domain.model.user.repository import UserRepository


@dataclass(frozen=True)
class ChangeContactsCommand:
    user_id: UUID
    email: str | None
    phone: int | None


class ChangeContacts:
    def __init__(self, event_bus: EventBus, repository: UserRepository, unit_of_work: UnitOfWork) -> None:
        self.event_bus = event_bus
        self.repository = repository
        self.unit_of_work = unit_of_work

    async def execute(self, command: ChangeContactsCommand) -> None:
        user = await self.repository.with_id(command.user_id)

        if not user:
            raise UserNotFoundError(message="User not found")

        if command.email and await self.repository.with_email(command.email):
            raise UserAlreadyExistsError(message="User already exists")

        if command.phone and await self.repository.with_phone(command.phone):
            raise UserAlreadyExistsError(message="User already exists")

        user.change_contacts(command.email, command.phone)

        await self.event_bus.publish(events=user.raise_events())
        await self.unit_of_work.commit()
