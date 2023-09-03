from typing import Optional

from sqlalchemy import insert, select, delete, Row

from app.models.user import user_account
from app.repositories.base_sql_alchemy_repository import BaseSqlAlchemyRepository
from app.schemas.user import User, UserInfo


class UserMapper:
    @staticmethod
    def row_to_user(row: Row):
        return User(
            user_id=row.user_id,
            user_info=UserInfo(
                user_name=row.user_name,
                first_name=row.first_name,
                last_name=row.last_name,
                email=row.email
            )
        )


class UserRepository(BaseSqlAlchemyRepository):
    async def create_user(
            self,
            user_name: str,
            first_name: Optional[str],
            last_name: Optional[str],
            email: Optional[str]
    ) -> User:
        insert_command = insert(user_account).values(
            user_name=user_name,
            first_name=first_name,
            last_name=last_name,
            email=email
        ).returning(user_account)

        async with self._db_connection.begin():
            row = (await self._db_connection.execute(insert_command)).one()

        return UserMapper.row_to_user(row)

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        select_command = select(user_account).where(user_account.c.user_id==user_id)

        async with self._db_connection.begin():
            row = (await self._db_connection.execute(select_command)).one_or_none()

        if not row:
            return None

        return UserMapper.row_to_user(row)

    async def update_user(
            self,
            user_id: int,
            first_name: Optional[str],
            last_name: Optional[str],
            email: Optional[str]
    ) -> Optional[User]:
        update_command = (
            user_account.update().
            values(
                first_name=first_name,
                last_name=last_name,
                email=email
            ).
            where(user_account.c.user_id == user_id)
        ).returning(user_account)

        async with self._db_connection.begin():
            row = (await self._db_connection.execute(update_command)).one_or_none()

        if not row:
            return None

        return UserMapper.row_to_user(row)

    async def delete_user(self, user_id: int) -> Optional[User]:
        delete_command = delete(user_account).where(user_account.c.user_id==user_id).returning(user_account)

        async with self._db_connection.begin():
            row = (await self._db_connection.execute(delete_command)).one_or_none()

        if not row:
            return None

        return UserMapper.row_to_user(row)
