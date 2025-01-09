from uuid import UUID

from app.domain.shared.base_entity import BaseEntity


class Skill(BaseEntity[UUID]):
    def __init__(
        self,
        skill_id: UUID,
        user_id: UUID,
        skill: str,
    ) -> None:
        super().__init__(skill_id)

        self.user_id = user_id
        self.skill_id = skill_id
        self.skill = skill
