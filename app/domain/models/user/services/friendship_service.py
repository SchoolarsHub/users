from app.domain.models.user.entities.user import User
from app.domain.models.user.exceptions.friendship_exceptions import (
    BlockerUserCannotAskForFriendshipError,
    CannotAddBlockedUserToFriendsError,
    CannotAddUserToFriendsTwiceError,
    CannotAddYourselfToFrinedsError,
    FriendshipRequestNotFoundError,
    YourFriendShipRequestAlreadyExistsError,
)


class FriendshipService:
    def ask_for_friendship(self, sender: User, receiver: User) -> None:
        if sender.entity_id == receiver.entity_id:
            raise CannotAddYourselfToFrinedsError(
                title="You cannot add yourself to friends",
            )

        if receiver in sender.blocked_users:
            raise CannotAddBlockedUserToFriendsError(
                title="You cannot add blocked user to friends",
            )

        if sender in receiver.blocked_users:
            raise BlockerUserCannotAskForFriendshipError(
                title=f"User with id: {receiver.entity_id} blocked you, can't make friendsip request",
            )

        if receiver in sender.frineds:
            raise CannotAddUserToFriendsTwiceError(
                title="You cannot add user to friends twice",
            )

        if receiver in sender.my_friendship_requests:
            raise YourFriendShipRequestAlreadyExistsError(
                title=f"Your friendship request to user {receiver.entity_id} already exists",
            )

        sender.my_friendship_requests.append(receiver)
        receiver.friendship_requests_to_me.append(receiver)

    def accept_friendship_request(self, sender: User, receiver: User) -> None:
        if sender not in receiver.my_friendship_requests:
            raise FriendshipRequestNotFoundError(
                title=f"Friendship request from user {sender.entity_id} not found",
            )

        receiver.my_friendship_requests.remove(sender)
        receiver.frineds.append(sender)

        sender.my_friendship_requests.remove(receiver)
        sender.frineds.append(receiver)

    def discard_friendship_request(self, sender: User, receiver: User) -> None:
        if sender not in receiver.my_friendship_requests:
            raise FriendshipRequestNotFoundError(
                title=f"Friendship request from user {sender.entity_id} not found",
            )

        receiver.friendship_requests_to_me.remove(sender)
        sender.my_friendship_requests.remove(receiver)
