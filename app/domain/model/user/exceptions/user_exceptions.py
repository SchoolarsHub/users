from app.domain.shared.exception import DomainError


class UserInactiveError(DomainError):
    pass


class InvalidUserAccountStatusError(DomainError):
    pass


class AddressValidationError(DomainError):
    pass


class ContactsValidationError(DomainError):
    pass


class UserNotFoundError(DomainError):
    pass
