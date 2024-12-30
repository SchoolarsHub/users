from dataclasses import dataclass
from uuid import UUID, uuid4

from app.application.common.event_bus import EventBus
from app.application.common.unit_of_work import UnitOfWork
from app.domain.model.user.entities.user import User
from app.domain.model.user.exceptions.user_exceptions import UserAlreadyExistsError
from app.domain.model.user.repositories.user_repository import UserRepository


@dataclass(frozen=True)
class CreateUserCommand:
    username: str
    bio: str | None
    city: str | None
    country: str | None
    email: str | None
    phone: int | None


class CreateUser:
    def __init__(self, unit_of_work: UnitOfWork, repository: UserRepository, event_bus: EventBus) -> None:
        self.unit_of_work = unit_of_work
        self.repository = repository
        self.event_bus = event_bus

    async def execute(self, command: CreateUserCommand) -> UUID:
        if command.phone and await self.repository.with_phone_number(phone_number=command.phone):
            raise UserAlreadyExistsError(title="User already exists")

        if command.email and await self.repository.with_email(email=command.email):
            raise UserAlreadyExistsError(title="User already exists")

        user = User.create_user(
            uuid=uuid4(), username=command.username, bio=command.bio, city=command.city, country=command.country, unit_of_work=self.unit_of_work
        )

        await self.event_bus.publish(events=user.raise_events())
        await self.unit_of_work.commit()

        return user.entity_id
