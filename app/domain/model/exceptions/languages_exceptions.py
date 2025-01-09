from app.domain.shared.exception import DomainError


class UserLanguageNotFoundError(DomainError):
    pass


class UserLanguageAlreadyExistsError(DomainError):
    pass
