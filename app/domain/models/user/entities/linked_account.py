from datetime import UTC, datetime
from typing import Self
from uuid import UUID

from app.domain.models.user.enums.social_networks import SocialNetworks
from app.domain.shared.unit_of_work import UnitOfWorkTracker
from app.domain.shared.uowed_entity import UowedEntity


class LinkedAccount(UowedEntity[UUID]):
    def __init__(
        self,
        linked_account_id: UUID,
        user_id: UUID,
        unit_of_work: UnitOfWorkTracker[Self],
        social_network: SocialNetworks,
        connection_link: str,
        connected_at: datetime,
    ) -> None:
        super().__init__(linked_account_id, unit_of_work)

        self.user_id = user_id
        self.social_network = social_network
        self.connection_link = connection_link
        self.connected_at = connected_at

    @classmethod
    def create_linked_account(
        cls: type[Self],
        user_id: UUID,
        linked_account_id: UUID,
        social_network: SocialNetworks,
        connection_link: str,
        unit_of_work: UnitOfWorkTracker[Self],
    ) -> Self:
        linked_account = cls(
            linked_account_id=linked_account_id,
            user_id=user_id,
            unit_of_work=unit_of_work,
            social_network=social_network,
            connection_link=connection_link,
            connected_at=datetime.now(UTC),
        )
        linked_account.mark_new()

        return linked_account

    def delete_linked_account(self) -> None:
        self.mark_deleted()
