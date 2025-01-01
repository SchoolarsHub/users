from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from app.domain.model.linked_account.social_networks import SocialNetworks
from app.domain.model.user.statuses import Statuses


@dataclass(frozen=True)
class LinkedAccountDTO:
    linked_account_id: UUID
    social_network: SocialNetworks
    connected_for: str | None
    connection_link: str
    connected_at: datetime


@dataclass(frozen=True)
class UserDTO:
    user_id: UUID
    status: Statuses
    created_at: datetime
    firstname: str
    lastname: str
    middlename: str | None
    linked_accounts: list[LinkedAccountDTO] = field(default_factory=list)
