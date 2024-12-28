from app.domain.models.user.exceptions.user_exceptions import ContactsValidationError


class Contacts:
    def __init__(
        self,
        phone: int | None = None,
        email: str | None = None,
    ) -> None:
        self.phone = phone
        self.email = email

        self.validate()

    def validate(self) -> None:
        if self.phone is None and self.email is None:
            raise ContactsValidationError("At least one contact must be provided")

        if self.phone is not None and not isinstance(self.phone, int):
            raise ContactsValidationError("Phone must be an integer")

        if self.email is not None and not isinstance(self.email, str):
            raise ContactsValidationError("Email must be a string")
