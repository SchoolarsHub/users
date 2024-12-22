from app.domain.models.user.exceptions.user_exceptions import ContactsValidationError


class Contacts:
    def __init__(self, phone_number: int | None, email: str | None) -> None:
        self.phone_number = phone_number
        self.email = email

        self.validate()

    def validate(self) -> None:
        if self.email is None and self.phone_number is None:
            raise ContactsValidationError("At least one contact must be provided")

        if self.email and not isinstance(self.email, str):
            raise ContactsValidationError("Email must be a non-empty string")

        if self.phone_number and not isinstance(self.phone_number, int):
            raise ContactsValidationError("Phone number must be a non-empty integer")

    def __str__(self) -> str:
        if self.email and self.phone_number:
            return f"Phone number: {self.phone_number}, Email: {self.email}"

        if self.email:
            return f"Email: {self.email}"

        if self.phone_number:
            return f"Phone number: {self.phone_number}"

        return "No contacts"
