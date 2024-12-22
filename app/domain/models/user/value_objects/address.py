from app.domain.models.user.exceptions.user_exceptions import AddressValidationError


class Address:
    def __init__(self, country: str, city: str, street: str, house_number: int, postal_code: int) -> None:
        self.country = country
        self.city = city
        self.street = street
        self.house_number = house_number
        self.postal_code = postal_code

        self.validate()

    def validate(self) -> None:
        if not self.country or not isinstance(self.country, str):
            raise AddressValidationError("Country must be a non-empty string")

        if not self.city or not isinstance(self.city, str):
            raise AddressValidationError("City must be a non-empty string")

        if not self.street or not isinstance(self.street, str):
            raise AddressValidationError("Street must be a non-empty string")

        if not isinstance(self.house_number, int) or self.house_number <= 0:
            raise AddressValidationError("House number must be a positive integer")

        if not isinstance(self.postal_code, int) or self.postal_code <= 0:
            raise AddressValidationError("Postal code must be a positive integer")

    def __str__(self) -> str:
        return f"{self.street} {self.house_number}, {self.postal_code} {self.city}, {self.country}"
