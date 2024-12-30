from dataclasses import dataclass

from app.domain.model.user.exceptions.user_exceptions import AddressValidationError


@dataclass(frozen=True)
class Address:
    city: str
    country: str

    def __post_init__(self) -> None:
        if not self.city:
            raise AddressValidationError("City cannot be empty")

        if not self.country:
            raise AddressValidationError("Country cannot be empty")

        if not isinstance(self.city, str):
            raise AddressValidationError("City must be a string")

        if not isinstance(self.country, str):
            raise AddressValidationError("Country must be a string")
