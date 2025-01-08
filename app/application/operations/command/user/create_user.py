from dataclasses import dataclass
from uuid import UUID, uuid4

from app.application.common.event_bus import EventBus
from app.application.common.unit_of_work import UnitOfWork
from app.domain.model.user.factory import UserFactory
from app.domain.model.user.repository import UserRepository


@dataclass(frozen=True)
class CreateUserCommand:
    email: str
    firstname: str
    lastname: str


class CreateUser:
    def __init__(self, event_bus: EventBus, repository: UserRepository, unit_of_work: UnitOfWork, factory: UserFactory) -> None:
        self.event_bus = event_bus
        self.repository = repository
        self.unit_of_work = unit_of_work
        self.factory = factory

    async def execute(self, command: CreateUserCommand) -> UUID:
        user = await self.factory.create_user(uuid4(), command.email, command.firstname, command.lastname)

        self.repository.add(user=user)
        await self.event_bus.publish(events=user.raise_events())
        await self.unit_of_work.commit()

        return user.user_id
