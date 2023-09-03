from typing import Optional

from pydantic import BaseModel


class UserInfo(BaseModel):
    user_name: str
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]


class User(BaseModel):
    user_id: int
    user_info: UserInfo


class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
