from sqlalchemy import UUID, BigInteger, Column, DateTime, ForeignKey, MetaData, String, Table

metadata = MetaData()


user_table = Table(
    "users",
    metadata,
    Column("user_id", UUID, primary_key=True, unique=True),
    Column("firstname", String(50), nullable=False),
    Column("lastname", String(50), nullable=False),
    Column("middlename", String(50), nullable=True),
    Column("email", String(50), nullable=True, unique=True),
    Column("phone", BigInteger, nullable=True, unique=True),
    Column("status", String(50), nullable=False),
    Column("created_at", DateTime, nullable=False),
    Column("deleted_at", DateTime, nullable=True),
)


linked_account_table = Table(
    "linked_accounts",
    metadata,
    Column("linked_account_id", UUID, primary_key=True, unique=True),
    Column("user_id", UUID, ForeignKey("users.user_id", ondelete="CASCADE")),
    Column("social_network", String(50), nullable=False),
    Column("connection_link", String, nullable=False),
    Column("connected_at", DateTime, nullable=False),
    Column("connection_reason", String, nullable=True),
)
