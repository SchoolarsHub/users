from collections.abc import Mapping, Sequence

from app.application.common.dto.user_dto import UserDTO
from app.application.common.unit_of_work import UnitOfWork
from app.domain.model.user.user import User
from app.domain.model.user.value_objects import Fullname


def convert_to_user_entity(rows: Sequence[Mapping], unit_of_work: UnitOfWork) -> User | None:
    if not rows:
        return None

    first_row = rows[0]

    user = User(
        user_id=first_row["user_id"],
        unit_of_work=unit_of_work,
        fullname=Fullname(firstname=first_row["firstname"], lastname=first_row["lastname"]),
        email=first_row["email"],
        status=first_row["status"],
        created_at=first_row["created_at"],
        deleted_at=first_row["deleted_at"],
    )

    return user


def convert_to_user_dto(rows: Sequence[Mapping]) -> UserDTO | None:
    if not rows:
        return None

    first_row = rows[0]

    user_dto = UserDTO(
        user_id=first_row["user_id"],
        firstname=first_row["firstname"],
        lastname=first_row["lastname"],
        status=first_row["status"],
        created_at=first_row["created_at"],
    )

    return user_dto
