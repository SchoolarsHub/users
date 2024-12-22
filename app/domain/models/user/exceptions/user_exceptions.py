from app.domain.common.exception import DomainError


class ContactsValidationError(DomainError):
    pass


class AddressValidationError(DomainError):
    pass
