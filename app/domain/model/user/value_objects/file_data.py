from dataclasses import dataclass

from app.domain.model.user.enums.file_extensions import FileExtensions
from app.domain.model.user.exceptions.avatar_exceptions import FileDataValidationError


@dataclass(frozen=True)
class FileData:
    filename: str
    file_extension: FileExtensions
    file_size: int

    def __post_init__(self) -> None:
        if not self.filename:
            raise FileDataValidationError("Filename cannot be empty")

        if not self.file_extension:
            raise FileDataValidationError("File extension cannot be empty")

        if not self.file_size:
            raise FileDataValidationError("File size cannot be empty")

        if not isinstance(self.file_size, int):
            raise FileDataValidationError("File size must be an integer")

        if not isinstance(self.file_extension, str):
            raise FileDataValidationError("File extension must be a string")

        if not isinstance(self.filename, str):
            raise FileDataValidationError("Filename must be a string")
