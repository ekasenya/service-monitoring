from sqlalchemy import String, Table, Column, Integer

from .metadata import metadata

user_account = Table(
    "user_account",
    metadata,
    Column("user_id", Integer, primary_key=True),
    Column("user_name", String, unique=True, nullable=False),
    Column("first_name", String),
    Column("last_name", String),
    Column("email", String),

)
