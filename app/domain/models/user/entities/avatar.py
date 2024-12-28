from typing import Self
from uuid import UUID

from app.domain.shared.unit_of_work import UnitOfWorkTracker
from app.domain.shared.uowed_entity import UowedEntity


class Avatar(UowedEntity[Self]):
    def __init__(
        self,
        avatar_id: UUID,
        user_id: UUID,
        unit_of_work: UnitOfWorkTracker[Self],
    ) -> None:
        super().__init__(avatar_id, unit_of_work)

        self.user_id = user_id

    @classmethod
    def create_avatar(cls: type[Self], user_id: UUID, unit_of_work: UnitOfWorkTracker[Self], avatar_id: UUID) -> Self:
        avatar = cls(avatar_id=avatar_id, user_id=user_id, unit_of_work=unit_of_work)
        avatar.mark_new()

        return avatar

    def delete_avatar(self) -> None:
        self.mark_deleted()
