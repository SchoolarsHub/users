from app.domain.shared.exception import DomainError


class InactiveUserError(DomainError):
    pass


class UserTemporarilyDeletedError(DomainError):
    pass


class UserAlreadyActiveError(DomainError):
    pass


class UserAlreadyExistsError(DomainError):
    pass


class UserNotFoundError(DomainError):
    pass
