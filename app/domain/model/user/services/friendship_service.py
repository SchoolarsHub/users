from uuid import UUID

from app.domain.model.user.enums.account_statuses import AccountStatuses
from app.domain.model.user.exceptions.friendship_exceptions import (
    BlockedUserCannotAskForFriendshipError,
    CannotAddBlockedUserToFriendsError,
    CannotAddUserToFriendsTwiceError,
    CannotAddYourselfToFrinedsError,
    FriendshipRequestNotFoundError,
)
from app.domain.model.user.exceptions.user_exceptions import UserInactiveError, UserNotFoundError
from app.domain.model.user.repositories.user_repository import UserRepository


class FriendshipService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def send_friendship_request(self, asker_id: UUID, receiver_id: UUID) -> None:
        if asker_id == receiver_id:
            raise CannotAddYourselfToFrinedsError(title="You cannot add yourself to friends")

        asker = await self.repository.with_id(asker_id)
        receiver = await self.repository.with_id(receiver_id)

        if not asker:
            raise UserNotFoundError(title=f"Asker user for friendship request with id: {asker_id} not found")

        if not receiver:
            raise UserNotFoundError(title=f"Reciever user for friendship request with id: {receiver_id} not found")

        if asker.account_status == AccountStatuses.INACTIVE:
            raise UserInactiveError(title=f"Asker user for friendship request with id: {asker_id} is inactive")

        if receiver.account_status == AccountStatuses.INACTIVE:
            raise UserInactiveError(title=f"Reciever user for friendship request with id: {receiver_id} is inactive")

        if asker.entity_id in receiver.blocked_users:
            raise BlockedUserCannotAskForFriendshipError(title="You cannot ask for friendship if you are blocked")

        if receiver.entity_id in asker.blocked_users:
            raise CannotAddBlockedUserToFriendsError(title="You cannot add blocked user to friends")

        if receiver.entity_id in asker.frineds:
            raise CannotAddUserToFriendsTwiceError(title="You cannot add user to friends twice")

        asker.sended_friendship_requests.append(receiver.entity_id)
        receiver.received_friendship_requests.append(asker.entity_id)

    async def accept_friendship_request(self, receiver_id: UUID, sender_id: UUID) -> None:
        if sender_id == receiver_id:
            raise CannotAddYourselfToFrinedsError(title="You cannot add yourself to friends")

        receiver = await self.repository.with_id(receiver_id)
        sender = await self.repository.with_id(sender_id)

        if not sender:
            raise UserNotFoundError(title=f"Asker user for friendship request with id: {sender_id} not found")

        if not receiver:
            raise UserNotFoundError(title=f"Reciever user for friendship request with id: {receiver_id} not found")

        if sender.entity_id not in receiver.received_friendship_requests:
            raise FriendshipRequestNotFoundError(title="Friendship request not found")

        sender.sended_friendship_requests.remove(receiver.entity_id)
        receiver.received_friendship_requests.remove(sender.entity_id)

        receiver.frineds.append(sender.entity_id)
        sender.frineds.append(receiver.entity_id)

    async def reject_friendship_request(self, receiver_id: UUID, sender_id: UUID) -> None:
        if sender_id == receiver_id:
            raise CannotAddYourselfToFrinedsError(title="You cannot add yourself to friends")

        receiver = await self.repository.with_id(receiver_id)
        sender = await self.repository.with_id(sender_id)

        if not sender:
            raise UserNotFoundError(title=f"Asker user for friendship request with id: {sender_id} not found")

        if not receiver:
            raise UserNotFoundError(title=f"Reciever user for friendship request with id: {receiver_id} not found")

        if sender.entity_id not in receiver.received_friendship_requests:
            raise FriendshipRequestNotFoundError(title="Friendship request not found")

        sender.sended_friendship_requests.remove(receiver.entity_id)
        receiver.received_friendship_requests.remove(sender.entity_id)
