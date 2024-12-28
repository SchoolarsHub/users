from app.domain.shared.exception import DomainError


class InvalidSocialNetworkError(DomainError):
    pass


class LinkedAccountUrlAlreadyExistsError(DomainError):
    pass


class LinkedAccountNotFoundError(DomainError):
    pass
