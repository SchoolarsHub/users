from dataclasses import dataclass

from app.domain.model.user.exceptions.user_exceptions import AddressValidationError


@dataclass(frozen=True)
class Address:
    city: str | None
    country: str | None

    def __post_init__(self) -> None:
        if not isinstance(self.city, str):
            raise AddressValidationError("City must be a string")

        if not isinstance(self.country, str):
            raise AddressValidationError("Country must be a string")
