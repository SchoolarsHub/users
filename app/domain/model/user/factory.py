from datetime import UTC, datetime
from uuid import UUID

from app.domain.model.user.events import UserCreated
from app.domain.model.user.exceptions import UserAlreadyExistsError
from app.domain.model.user.repository import UserRepository
from app.domain.model.user.statuses import Statuses
from app.domain.model.user.user import User
from app.domain.model.user.value_objects import Contacts, Fullname
from app.domain.shared.unit_of_work import UnitOfWorkTracker


class UserFactory:
    def __init__(self, repository: UserRepository, unit_of_work: UnitOfWorkTracker) -> None:
        self.repository = repository
        self.unit_of_work = unit_of_work

    async def create_user(self, user_id: UUID, email: str | None, phone: int | None, firstname: str, lastname: str, middlename: str | None) -> User:
        if email and await self.repository.with_email(email):
            raise UserAlreadyExistsError(message="User already exists")

        if phone and await self.repository.with_phone(phone):
            raise UserAlreadyExistsError(message="User already exists")

        fullname = Fullname(firstname=firstname, lastname=lastname, middlename=middlename)
        contacts = Contacts(email=email, phone=phone)
        user = User(user_id, self.unit_of_work, fullname, contacts, Statuses.ACTIVE, [], datetime.now(UTC))
        user.record_event(UserCreated(user.user_id, firstname, lastname, middlename, user.status))

        return user
