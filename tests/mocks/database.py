from typing import TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from app.domain.model.linked_account.linked_account import LinkedAccount
    from app.domain.model.user.user import User


class FakeDatabase:
    def __init__(self) -> None:
        self.users: dict[UUID, User] = {}
        self.linked_accounts: dict[UUID, LinkedAccount] = {}
