from app.domain.shared.exception import DomainError


class CannotAddYourselfToFrinedsError(DomainError):
    pass


class CannotAddUserToFriendsTwiceError(DomainError):
    pass


class FriendshipRequestNotFoundError(DomainError):
    pass
