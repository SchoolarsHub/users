from app.domain.models.user.enums.file_extensions import FileExtensions
from app.domain.models.user.exceptions.avatar_exceptions import FileDataValidationError


class FileData:
    def __init__(
        self,
        filename: str,
        file_extension: FileExtensions,
        file_size: int,
    ) -> None:
        self.filename = filename
        self.file_extension = file_extension
        self.file_size = file_size

        self.validate()

    def validate(self) -> None:
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
