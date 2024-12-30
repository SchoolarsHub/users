from uuid import uuid4

from app.domain.model.user.entities.friendship import Friendship
from app.domain.model.user.entities.user import User
from app.domain.model.user.enums.account_statuses import AccountStatuses
from app.domain.model.user.enums.friendship_status import FriendshipStatus
from app.domain.model.user.exceptions.friendship_exceptions import (
    CannotAddUserToFriendsTwiceError,
    CannotAddYourselfToFrinedsError,
    FriendshipRequestNotFoundError,
)
from app.domain.model.user.exceptions.user_exceptions import UserInactiveError
from app.domain.shared.unit_of_work import UnitOfWorkTracker


class FriendshipService:
    def __init__(self, unit_of_work: UnitOfWorkTracker) -> None:
        self.unit_of_work = unit_of_work

    async def send_friendship_request(self, sender_friendship: User, receiver_friendship: User) -> None:
        if sender_friendship.entity_id == receiver_friendship.entity_id:
            raise CannotAddYourselfToFrinedsError(title="You cannot add yourself to friends")

        if sender_friendship.account_status == AccountStatuses.INACTIVE:
            raise UserInactiveError(title="Sender is inactive")

        for sended_friendship_request in sender_friendship.sended_friendship_requests:
            if sended_friendship_request.receiver_user_id == receiver_friendship.entity_id:
                raise CannotAddUserToFriendsTwiceError(title="You have already sent a friendship request to this user")

        for friend in sender_friendship.friends:
            if friend.receiver_user_id == receiver_friendship.entity_id:
                raise CannotAddUserToFriendsTwiceError(title="You are already friends with this user")

        friendship = Friendship.create_friendship(
            friendship_id=uuid4(),
            suggested_user_id=sender_friendship.entity_id,
            receiver_user_id=receiver_friendship.entity_id,
            unit_of_work=self.unit_of_work,
        )

        sender_friendship.sended_friendship_requests.append(friendship.entity_id)
        receiver_friendship.received_friendship_requests.append(friendship.entity_id)

    async def accept_friendship_request(self, sender_friendship: User, receiver_friendship: User) -> None:
        if sender_friendship.entity_id == receiver_friendship.entity_id:
            raise CannotAddYourselfToFrinedsError(title="You cannot add yourself to friends")

        if receiver_friendship.account_status == AccountStatuses.INACTIVE:
            raise UserInactiveError(title="Receiver is inactive")

        for received_friendship_request in receiver_friendship.received_friendship_requests:
            if received_friendship_request.receiver_user_id == received_friendship_request.entity_id:
                received_friendship_request.change_friendship_status(new_status=FriendshipStatus.ACCEPTED)

                sender_friendship.sended_friendship_requests.remove(received_friendship_request.entity_id)
                receiver_friendship.received_friendship_requests.remove(received_friendship_request.entity_id)

                sender_friendship.friends.append(received_friendship_request)
                receiver_friendship.friends.append(received_friendship_request)

                received_friendship_request.delete_friendship()

        raise FriendshipRequestNotFoundError(title="Friendship request not found")

    async def decline_friendship_request(self, sender_friendship: User, receiver_friendship: User) -> None:
        if sender_friendship.entity_id == receiver_friendship.entity_id:
            raise CannotAddYourselfToFrinedsError(title="You cannot add yourself to friends")

        if receiver_friendship.account_status == AccountStatuses.INACTIVE:
            raise UserInactiveError(title="Receiver is inactive")

        for received_friendship_request in receiver_friendship.received_friendship_requests:
            if received_friendship_request.receiver_user_id == received_friendship_request.entity_id:
                sender_friendship.sended_friendship_requests.remove(received_friendship_request)
                receiver_friendship.received_friendship_requests.remove(received_friendship_request)

                received_friendship_request.delete_friendship()

        raise FriendshipRequestNotFoundError(title="Friendship request not found")

    async def cancel_friendship_request(self, sender_friendship: User, receiver_friendship: User) -> None:
        if sender_friendship.entity_id == receiver_friendship.entity_id:
            raise CannotAddYourselfToFrinedsError(title="You cannot add yourself to friends")

        if sender_friendship.account_status == AccountStatuses.INACTIVE:
            raise UserInactiveError(title="Sender is inactive")

        for sended_friendship_request in sender_friendship.sended_friendship_requests:
            if sended_friendship_request.receiver_user_id == receiver_friendship.entity_id:
                sender_friendship.sended_friendship_requests.remove(sended_friendship_request)
                receiver_friendship.received_friendship_requests.remove(sended_friendship_request)

                sended_friendship_request.delete_friendship()

        raise FriendshipRequestNotFoundError(title="Friendship request not found")
