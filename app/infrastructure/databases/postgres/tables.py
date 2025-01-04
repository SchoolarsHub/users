from sqlalchemy import UUID, BigInteger, Column, DateTime, ForeignKey, MetaData, String, Table
from sqlalchemy.orm import registry

metadata = MetaData()
mapper_registry = registry(metadata=metadata)


user_table = Table(
    "users",
    mapper_registry.metadata,
    Column("user_id", UUID, primary_key=True, unique=True),
    Column("firstname", String(50), nullable=False),
    Column("lastname", String(50), nullable=False),
    Column("middlename", String(50), nullable=True),
    Column("email", String(50), nullable=True, unique=True),
    Column("phone", BigInteger, nullable=True, unique=True),
    Column("status", String(50), nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("deleted_at", DateTime(timezone=True), nullable=True),
)


linked_account_table = Table(
    "linked_accounts",
    mapper_registry.metadata,
    Column("linked_account_id", UUID, primary_key=True, unique=True),
    Column("user_id", UUID, ForeignKey("users.user_id", ondelete="CASCADE")),
    Column("social_network", String(50), nullable=False),
    Column("connection_link", String, nullable=False),
    Column("connected_at", DateTime(timezone=True), nullable=False),
    Column("connection_reason", String, nullable=True),
)
