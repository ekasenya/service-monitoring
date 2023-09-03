from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncConnection

from app.db.engine import engine
from app.repositories.user_repository import UserRepository


async def get_connection() -> AsyncGenerator[AsyncConnection, None]:
    async with engine.connect() as connection:
        yield connection


async def get_user_repository(db_connection: AsyncConnection = Depends(get_connection)):
    return UserRepository(db_connection=db_connection)
