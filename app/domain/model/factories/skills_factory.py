from uuid import UUID, uuid4

from app.domain.model.entities.skill import Skill
from app.domain.model.exceptions.skills_exceptions import UserSkillAlreadyExistsError
from app.domain.model.exceptions.user_exceptions import UserNotFoundError
from app.domain.model.repositories.skills_repository import SkillsRepository
from app.domain.model.repositories.user_repository import UserRepository


class SkillFactory:
    def __init__(self, skill_repository: SkillsRepository, user_repository: UserRepository) -> None:
        self.skill_repository = skill_repository
        self.user_repository = user_repository

    async def create_skill(self, user_id: UUID, skill: str) -> Skill:
        user = await self.user_repository.with_id(user_id)

        if not user:
            raise UserNotFoundError(message=f"User with id: {user_id} not found")

        user.check_user_status()

        user_skills = await self.skill_repository.with_user_id(user_id)

        for user_skill in user_skills:
            if user_skill.skill.lower() == skill.lower():
                raise UserSkillAlreadyExistsError(message=f"User with id: {user_id} already has skill: {skill}")

        skill_id = uuid4()

        return Skill(skill_id, user_id, skill)
