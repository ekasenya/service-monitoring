import os
from pydantic import PostgresDsn
from sqlalchemy.ext.asyncio import create_async_engine


engine = create_async_engine(
    url=PostgresDsn.build(
        scheme="postgresql+asyncpg",
        host=os.environ['DB_HOST'],
        port=os.environ['DB_PORT'],
        path=f"/{os.environ['DB_NAME']}",
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD']
    )
)
