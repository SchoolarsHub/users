from dataclasses import dataclass
from uuid import UUID

from app.application.common.event_bus import EventBus
from app.application.common.unit_of_work import UnitOfWork
from app.domain.model.user.exceptions.user_exceptions import UserNotFoundError
from app.domain.model.user.repositories.user_repository import UserRepository
from app.domain.model.user.services.friendship_service import FriendshipService


@dataclass(frozen=True)
class CancelFriendshipRequestCommand:
    user_id: UUID
    receiver_id: UUID


class CancelFriendshipRequest:
    def __init__(self, unit_of_work: UnitOfWork, friendship_service: FriendshipService, event_bus: EventBus, repository: UserRepository) -> None:
        self.unit_of_work = unit_of_work
        self.friendship_service = friendship_service
        self.event_bus = event_bus
        self.repository = repository

    async def execute(self, command: CancelFriendshipRequestCommand) -> None:
        sender = await self.repository.with_id(uuid=command.user_id)

        if not sender:
            raise UserNotFoundError(f"User with id {command.user_id} not found")

        receiver = await self.repository.with_id(uuid=command.receiver_id)

        if not receiver:
            raise UserNotFoundError(f"User with id {command.receiver_id} not found")

        await self.friendship_service.cancel_friendship_request(sender_friendship=sender, receiver_friendship=receiver)
        await self.event_bus.publish(events=sender.raise_events())
        await self.unit_of_work.commit()
