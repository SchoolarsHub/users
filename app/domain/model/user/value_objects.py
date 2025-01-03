from dataclasses import dataclass

from app.domain.model.user.exceptions import ContactsValidationError


@dataclass(frozen=True)
class Contacts:
    email: str | None
    phone: int | None

    def __post_init__(self) -> None:
        if self.email is None and self.phone is None:
            raise ContactsValidationError(message="At least one contact must be provided: email or phone")


@dataclass(frozen=True)
class Fullname:
    firstname: str
    lastname: str
    middlename: str | None
