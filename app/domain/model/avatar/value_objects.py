from dataclasses import dataclass

from app.domain.model.avatar.exceptions import FileDataValidationError
from app.domain.model.avatar.extensions import Extensions


@dataclass(frozen=True)
class FileData:
    extension: Extensions
    size: int

    def __post_init__(self) -> None:
        if self.size > 5 * 1024 * 1024:
            raise FileDataValidationError("Photo size must be less than 5 MB")

        if self.extension not in list(Extensions):
            raise FileDataValidationError("Invalid photo extension")
