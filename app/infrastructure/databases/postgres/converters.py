from collections.abc import Mapping, Sequence

from app.application.common.dto.user_dto import LinkedAccountDTO, UserDTO
from app.application.common.unit_of_work import UnitOfWork
from app.domain.model.linked_account.linked_account import LinkedAccount
from app.domain.model.linked_account.social_networks import SocialNetworks
from app.domain.model.user.user import User
from app.domain.model.user.value_objects import Contacts, Fullname


def convert_to_user_entity(rows: Sequence[Mapping], unit_of_work: UnitOfWork) -> User | None:
    if not rows:
        return None

    first_row = rows[0]

    user = User(
        user_id=first_row["user_id"],
        unit_of_work=unit_of_work,
        fullname=Fullname(firstname=first_row["firstname"], lastname=first_row["lastname"], middlename=first_row["middlename"]),
        contacts=Contacts(email=first_row["email"], phone=first_row["phone"]),
        status=first_row["status"],
        created_at=first_row["created_at"],
        deleted_at=first_row["deleted_at"],
        linked_accounts=[
            LinkedAccount(
                linked_account_id=row["linked_account_id"],
                user_id=row["user_id"],
                social_network=SocialNetworks(row["social_network"]),
                connection_link=row["connection_link"],
                unit_of_work=unit_of_work,
                connected_at=row["connected_at"],
                connected_for=row["connection_reason"],
            )
            for row in rows
            if row["linked_account_id"]
        ],
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
        middlename=first_row["middlename"],
        status=first_row["status"],
        created_at=first_row["created_at"],
        linked_accounts=[
            LinkedAccountDTO(
                linked_account_id=row["linked_account_id"],
                social_network=SocialNetworks(row["social_network"]),
                connection_link=row["connection_link"],
                connected_at=row["connected_at"],
                connected_for=row["connection_reason"],
            )
            for row in rows
            if row["linked_account_id"]
        ],
    )

    return user_dto
