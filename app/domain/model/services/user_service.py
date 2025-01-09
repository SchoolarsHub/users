from uuid import UUID

from app.domain.model.entities.user import User
from app.domain.model.exceptions.user_exceptions import UserAlreadyExistsError, UserNotFoundError
from app.domain.model.repositories.user_repository import UserRepository
from app.domain.model.services.language_service import LanguageService
from app.domain.model.services.skill_service import SkillService


class UserService:
    def __init__(self, user_repository: UserRepository, language_service: LanguageService, skill_service: SkillService) -> None:
        self.user_repository = user_repository
        self.skill_service = skill_service
        self.language_service = language_service

    async def change_email(self, user_id: UUID, new_email: str) -> User:
        user = await self.user_repository.with_id(user_id)

        if not user:
            raise UserNotFoundError(message=f"User with id: {user_id} not found")

        if await self.user_repository.with_email(new_email):
            raise UserAlreadyExistsError(message="User already exists")

        user.change_email(new_email)

        return user

    async def delete_user_permanently(self, user_id: UUID) -> User:
        user = await self.user_repository.with_id(user_id)

        if not user:
            raise UserNotFoundError(message=f"User with id: {user_id} not found")

        await self.skill_service.delete_all_user_skills(user_id)
        await self.language_service.delete_all_user_languages(user_id)

        user.delete_user_permanently()

        return user
