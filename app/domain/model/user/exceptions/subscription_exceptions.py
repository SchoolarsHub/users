from app.domain.shared.exception import DomainError


class CannotSubscibeToYourselfError(DomainError):
    pass


class SubscriptionAlreadyExistsError(DomainError):
    pass


class SubscriptionNotFoundError(DomainError):
    pass


class CannotUnsubscribeFromYourselfError(DomainError):
    pass


class CannotRemoveFromSubscribersYourselfError(DomainError):
    pass
