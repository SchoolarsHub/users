from sqlalchemy.orm import composite, registry, relationship

from app.domain.model.linked_account.linked_account import LinkedAccount
from app.domain.model.user.user import User
from app.domain.model.user.value_objects import Contacts, Fullname
from app.infrastructure.databases.postgres.tables import linked_account_table, metadata, user_table

mapper_registry = registry(metadata)


mapper_registry.map_imperatively(
    User,
    user_table,
    properties={
        "linked_accounts": relationship(LinkedAccount, backref="user", cascade="all, delete-orphan"),
        "contacts": composite(Contacts, user_table.c.email, user_table.c.phone_number),
        "fullname": composite(Fullname, user_table.c.firstname, user_table.c.lastname, user_table.c.middlename),
    },
)


mapper_registry.map_imperatively(LinkedAccount, linked_account_table, properties={"user": relationship(User, back_populates="linked_accounts")})
