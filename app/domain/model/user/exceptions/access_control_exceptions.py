from app.domain.shared.exception import DomainError


class CannotBlockYourselfError(DomainError):
    pass


class CannotBlockUserTwiceError(DomainError):
    pass


class BlockedUserNotFoundError(DomainError):
    pass
