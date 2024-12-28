from typing import Self
from uuid import UUID

from app.domain.shared.unit_of_work import UnitOfWorkTracker
from app.domain.shared.uowed_entity import UowedEntity


class LinkedAccount(UowedEntity[UUID]):
    def __init__(
        self,
        linked_account_id: UUID,
        user_id: UUID,
        unit_of_work: UnitOfWorkTracker[Self],
    ) -> None:
        super().__init__(linked_account_id, unit_of_work)

        self.user_id = user_id

    @classmethod
    def create_linked_account(
        cls: type[Self],
        user_id: UUID,
        linked_account_id: UUID,
        unit_of_work: UnitOfWorkTracker[Self],
    ) -> Self:
        linked_account = cls(
            linked_account_id=linked_account_id,
            user_id=user_id,
            unit_of_work=unit_of_work,
        )
        linked_account.mark_new()

        return linked_account

    def delete_linked_account(self) -> None:
        self.mark_deleted()
