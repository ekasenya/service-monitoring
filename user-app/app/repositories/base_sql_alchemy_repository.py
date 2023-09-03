from sqlalchemy.ext.asyncio import AsyncConnection


class BaseSqlAlchemyRepository:
    def __init__(self, db_connection: AsyncConnection):
        super().__init__()
        self._db_connection = db_connection