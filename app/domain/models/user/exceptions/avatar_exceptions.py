from app.domain.shared.exception import DomainError


class InvalidAvatarFileExtensionError(DomainError):
    pass


class AvatarNotFoundError(DomainError):
    pass


class FileDataValidationError(DomainError):
    pass
