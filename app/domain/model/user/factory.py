from datetime import UTC, datetime
from uuid import uuid4

from app.domain.model.user.enums import Statuses
from app.domain.model.user.events import UserCreated
from app.domain.model.user.exceptions import UserAlreadyExistsError
from app.domain.model.user.repository import UserRepository
from app.domain.model.user.user import User
from app.domain.model.user.value_objects import Fullname
from app.domain.shared.unit_of_work import UnitOfWorkTracker


class UserFactory:
    def __init__(self, repository: UserRepository, unit_of_work: UnitOfWorkTracker) -> None:
        self.repository = repository
        self.unit_of_work = unit_of_work

    async def create_user(self, email: str, firstname: str, lastname: str) -> User:
        if await self.repository.with_email(email):
            raise UserAlreadyExistsError(message="User already exists")

        fullname = Fullname(firstname=firstname, lastname=lastname)
        user = User(uuid4(), self.unit_of_work, fullname, email, Statuses.ACTIVE, datetime.now(UTC))
        user.record_event(UserCreated(user.user_id, firstname, lastname, email, user.status))

        return user
