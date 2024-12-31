from app.domain.shared.exception import DomainError


class ConnectionLinkNotBelongsToSocialNetworkError(DomainError):
    pass


class LinkedAccountAlreadyExistsError(DomainError):
    pass


class LinkedAccountNotExistsError(DomainError):
    pass


class InvalidSocialNetworkError(DomainError):
    pass
