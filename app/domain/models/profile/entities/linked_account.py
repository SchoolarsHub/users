from datetime import UTC, datetime
from typing import Self
from uuid import UUID

from app.domain.common.unit_of_work import UnitOfWorkTracker
from app.domain.common.uowed_entity import UowedEntity
from app.domain.models.profile.enums.allowed_accounts import AllowedAccounts


class LinkedAccount(UowedEntity[UUID]):
    def __init__(
        self,
        linked_account_id: UUID,
        profile_id: UUID,
        linked_account_name: AllowedAccounts,
        linked_account_url: str,
        linked_at: datetime,
        unit_of_work: UnitOfWorkTracker[Self],
    ) -> None:
        super().__init__(linked_account_id, unit_of_work)

        self.profile_id = profile_id
        self.linked_account_name = linked_account_name
        self.linked_account_url = linked_account_url
        self.linked_at = linked_at

    @classmethod
    def create_linked_account(
        cls: type[Self],
        profile_id: UUID,
        linked_account_id: UUID,
        linked_account_name: AllowedAccounts,
        linked_account_url: str,
        unit_of_work: UnitOfWorkTracker[Self],
    ) -> Self:
        linked_account = cls(
            linked_account_id=linked_account_id,
            profile_id=profile_id,
            unit_of_work=unit_of_work,
            linked_account_name=linked_account_name,
            linked_account_url=linked_account_url,
            linked_at=datetime.now(UTC),
        )
        linked_account.mark_new()

        return linked_account

    def delete_linked_account(self) -> None:
        self.mark_deleted()
