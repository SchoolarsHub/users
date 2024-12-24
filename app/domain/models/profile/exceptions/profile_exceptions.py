from app.domain.common.exception import DomainError


class AvatarNotFoundError(DomainError):
    pass


class LinkedAccountNotFoundError(DomainError):
    pass


class FullnameValidationError(DomainError):
    pass


class InvalidProfileTypeError(DomainError):
    pass


class InvalidFileExtensionError(DomainError):
    pass


class InvalidLinkedAccountNameError(DomainError):
    pass
