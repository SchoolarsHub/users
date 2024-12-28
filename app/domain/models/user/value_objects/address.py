from app.domain.models.user.exceptions.user_exceptions import AddressValidationError


class Address:
    def __init__(
        self,
        city: str,
        country: str,
    ) -> None:
        self.city = city
        self.country = country

        self.validate()

    def validate(self) -> None:
        if not self.city:
            raise AddressValidationError("City cannot be empty")

        if not self.country:
            raise AddressValidationError("Country cannot be empty")

        if not isinstance(self.city, str):
            raise AddressValidationError("City must be a string")

        if not isinstance(self.country, str):
            raise AddressValidationError("Country must be a string")
