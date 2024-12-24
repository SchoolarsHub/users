from typing import Self
from uuid import UUID

from app.domain.common.unit_of_work import UnitOfWorkTracker
from app.domain.common.uowed_entity import UowedEntity
from app.domain.models.profile.enums.allowed_extensions import AllowedExtensions


class Avatar(UowedEntity[UUID]):
    def __init__(
        self,
        avatar_id: UUID,
        profile_id: UUID,
        unit_of_work: UnitOfWorkTracker[Self],
        file_name: str,
        file_size: int,
        file_extension: AllowedExtensions,
    ) -> None:
        super().__init__(avatar_id, unit_of_work)

        self.profile_id = profile_id
        self.file_name = file_name
        self.file_size = file_size
        self.file_extension = file_extension

    @classmethod
    def create_avatar(
        cls: type[Self],
        profile_id: UUID,
        avatar_id: UUID,
        unit_of_work: UnitOfWorkTracker[Self],
        file_name: str,
        file_size: int,
        file_extension: AllowedExtensions,
    ) -> Self:
        avatar = cls(
            avatar_id=avatar_id,
            profile_id=profile_id,
            unit_of_work=unit_of_work,
            file_name=file_name,
            file_size=file_size,
            file_extension=file_extension,
        )
        avatar.mark_new()

        return avatar

    def delete_avatar(self) -> None:
        self.mark_deleted()
