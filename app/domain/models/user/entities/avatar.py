from datetime import UTC, datetime
from typing import Self
from uuid import UUID

from app.domain.models.user.value_objects.file_data import FileData
from app.domain.shared.unit_of_work import UnitOfWorkTracker
from app.domain.shared.uowed_entity import UowedEntity


class Avatar(UowedEntity[Self]):
    def __init__(
        self,
        avatar_id: UUID,
        user_id: UUID,
        unit_of_work: UnitOfWorkTracker,
        file_data: FileData,
        file: bytes,
        uploaded_at: datetime,
    ) -> None:
        super().__init__(avatar_id, unit_of_work)

        self.user_id = user_id
        self.file_data = file_data
        self.uploaded_at = uploaded_at
        self.file = file

    @classmethod
    def create_avatar(
        cls: type[Self],
        user_id: UUID,
        unit_of_work: UnitOfWorkTracker,
        avatar_id: UUID,
        file_data: FileData,
        file: bytes,
    ) -> Self:
        avatar = cls(
            avatar_id=avatar_id,
            user_id=user_id,
            unit_of_work=unit_of_work,
            file_data=file_data,
            file=file,
            uploaded_at=datetime.now(UTC),
        )
        avatar.mark_new()

        return avatar

    def delete_avatar(self) -> None:
        self.mark_deleted()
