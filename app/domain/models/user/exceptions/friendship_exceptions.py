from app.domain.shared.exception import DomainError


class CannotAddYourselfToFrinedsError(DomainError):
    pass


class CannotAddBlockedUserToFriendsError(DomainError):
    pass


class CannotAddUserToFriendsTwiceError(DomainError):
    pass


class YourFriendShipRequestAlreadyExistsError(DomainError):
    pass


class BlockerUserCannotAskForFriendshipError(DomainError):
    pass


class FriendshipRequestNotFoundError(DomainError):
    pass
