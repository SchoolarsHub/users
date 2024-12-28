from app.domain.shared.exception import DomainError


class CannotSubscibeToYourselfError(DomainError):
    pass


class SubscriptionAlreadyExistsError(DomainError):
    pass


class CannotSubscibeToBlockedUserError(DomainError):
    pass


class BlockedUserCannotSubscribeError(DomainError):
    pass


class SubscriptionNotFoundError(DomainError):
    pass
