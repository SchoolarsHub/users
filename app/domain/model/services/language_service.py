from uuid import UUID

from app.domain.model.exceptions.languages_exceptions import UserLanguageNotFoundError
from app.domain.model.exceptions.user_exceptions import UserNotFoundError
from app.domain.model.repositories.languages_repository import LanguagesRepository
from app.domain.model.repositories.user_repository import UserRepository


class LanguageService:
    def __init__(self, language_repository: LanguagesRepository, user_repository: UserRepository) -> None:
        self.language_repository = language_repository
        self.user_repository = user_repository

    async def delete_language(self, user_id: UUID, language_id: UUID) -> None:
        user = await self.user_repository.with_id(user_id)

        if not user:
            raise UserNotFoundError(message=f"User with id: {user_id} not found")

        user.check_user_status()

        user_language = await self.language_repository.with_id(language_id)

        if not user_language:
            raise UserLanguageNotFoundError(message=f"User with id: {user_id} does not have language with id: {language_id}")

        self.language_repository.delete(user_language)

    async def delete_all_user_languages(self, user_id: UUID) -> None:
        user = await self.user_repository.with_id(user_id)

        if not user:
            raise UserNotFoundError(message=f"User with id: {user_id} not found")

        user_languages = await self.language_repository.with_user_id(user_id)

        for user_language in user_languages:
            self.language_repository.delete(user_language)
