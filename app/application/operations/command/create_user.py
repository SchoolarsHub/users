from dataclasses import dataclass
from uuid import UUID, uuid4

from app.application.common.event_bus import EventBus
from app.application.common.unit_of_work import UnitOfWork
from app.domain.model.user.exceptions import UserAlreadyExistsError
from app.domain.model.user.repository import UserRepository
from app.domain.model.user.user import User


@dataclass(frozen=True)
class CreateUserCommand:
    phone: int | None
    email: str | None
    firstname: str
    lastname: str
    middlename: str | None


class CreateUser:
    def __init__(self, event_bus: EventBus, repository: UserRepository, unit_of_work: UnitOfWork) -> None:
        self.event_bus = event_bus
        self.repository = repository
        self.unit_of_work = unit_of_work

    async def execute(self, command: CreateUserCommand) -> UUID:
        if command.email and await self.repository.with_email(command.email):
            raise UserAlreadyExistsError(title="User already exists")

        if command.phone and await self.repository.with_phone(command.phone):
            raise UserAlreadyExistsError(title="User already exists")

        user = User.create_user(uuid4(), command.firstname, command.lastname, command.middlename, command.email, command.phone, self.unit_of_work)

        await self.repository.add(user=user)
        await self.event_bus.publish(events=user.raise_events())
        await self.unit_of_work.commit()

        return user.user_id
