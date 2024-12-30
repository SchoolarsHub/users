from datetime import UTC, datetime
from typing import Self
from uuid import UUID

from app.domain.model.user.enums.friendship_status import FriendshipStatus
from app.domain.shared.unit_of_work import UnitOfWorkTracker
from app.domain.shared.uowed_entity import UowedEntity


class Friendship(UowedEntity[UUID]):
    def __init__(
        self,
        friendship_id: UUID,
        suggested_user_id: UUID,
        receiver_user_id: UUID,
        suggested_at: datetime,
        unit_of_work: UnitOfWorkTracker,
        friendship_status: FriendshipStatus,
    ) -> None:
        super().__init__(friendship_id, unit_of_work)

        self.suggected_user_id = suggested_user_id
        self.receiver_user_id = receiver_user_id
        self.suggested_at = suggested_at
        self.friendship_status = friendship_status

    @classmethod
    def create_friendship(
        cls: type[Self],
        friendship_id: UUID,
        suggested_user_id: UUID,
        receiver_user_id: UUID,
        unit_of_work: UnitOfWorkTracker,
    ) -> Self:
        friendship = cls(
            friendship_id=friendship_id,
            suggested_user_id=suggested_user_id,
            receiver_user_id=receiver_user_id,
            suggested_at=datetime.now(UTC),
            unit_of_work=unit_of_work,
            friendship_status=FriendshipStatus.PENDING,
        )
        friendship.mark_new()

        return friendship

    def delete_friendship(self) -> None:
        self.mark_deleted()
