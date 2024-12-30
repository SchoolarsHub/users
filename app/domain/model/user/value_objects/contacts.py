from dataclasses import dataclass

from app.domain.model.user.exceptions.user_exceptions import ContactsValidationError


@dataclass(frozen=True)
class Contacts:
    phone: int | None
    email: str | None

    def __post_init__(self) -> None:
        if self.phone is None and self.email is None:
            raise ContactsValidationError("At least one contact must be provided")

        if self.phone is not None and not isinstance(self.phone, int):
            raise ContactsValidationError("Phone must be an integer")

        if self.email is not None and not isinstance(self.email, str):
            raise ContactsValidationError("Email must be a string")
