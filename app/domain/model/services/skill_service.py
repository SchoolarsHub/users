from uuid import UUID

from app.domain.model.exceptions.skills_exceptions import UserSkillNotFoundError
from app.domain.model.exceptions.user_exceptions import UserNotFoundError
from app.domain.model.repositories.skills_repository import SkillsRepository
from app.domain.model.repositories.user_repository import UserRepository


class SkillService:
    def __init__(self, user_repository: UserRepository, skill_repository: SkillsRepository) -> None:
        self.user_repository = user_repository
        self.skill_repository = skill_repository

    async def delete_skill(self, user_id: UUID, skill_id: UUID) -> None:
        user = await self.user_repository.with_id(user_id)

        if not user:
            raise UserNotFoundError(message=f"User with id: {user_id} not found")

        user.check_user_status()

        user_skill = await self.skill_repository.with_id(skill_id)

        if not user_skill:
            raise UserSkillNotFoundError(message=f"User with id: {user_id} does not have skill with id: {skill_id}")

        self.skill_repository.delete(user_skill)

    async def delete_all_user_skills(self, user_id: UUID) -> None:
        user = await self.user_repository.with_id(user_id)

        if not user:
            raise UserNotFoundError(message=f"User with id: {user_id} not found")

        user_skills = await self.skill_repository.with_user_id(user_id)

        for user_skill in user_skills:
            self.skill_repository.delete(user_skill)
