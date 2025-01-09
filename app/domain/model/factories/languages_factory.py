from uuid import UUID, uuid4

from app.domain.model.entities.language import Language
from app.domain.model.enums.languages import Languages
from app.domain.model.exceptions.languages_exceptions import UserLanguageAlreadyExistsError
from app.domain.model.exceptions.user_exceptions import UserNotFoundError
from app.domain.model.repositories.languages_repository import LanguagesRepository
from app.domain.model.repositories.user_repository import UserRepository


class LanguageFactory:
    def __init__(self, language_repository: LanguagesRepository, user_repository: UserRepository) -> None:
        self.language_repository = language_repository
        self.user_repository = user_repository

    async def create_language(self, user_id: UUID, language: Languages) -> Language:
        user = await self.user_repository.with_id(user_id)

        if not user:
            raise UserNotFoundError(message=f"User with id: {user_id} not found")

        user.check_user_status()

        user_languages = await self.language_repository.with_user_id(user_id)

        for user_language in user_languages:
            if user_language.language.lower() == language.lower():
                raise UserLanguageAlreadyExistsError(message=f"User with id: {user_id} already has language: {language}")

        language_id = uuid4()

        return Language(language_id, user_id, language)
