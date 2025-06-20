import nuvie_db.nuvie.core as mc

from nuvie_db.nuvie import metadata
from sqlmodel import Field, SQLModel


class UserBase(mc.BaseModelNuvie_):
    password: str = Field(nullable=True)
    user_name: str = Field(
        nullable=False, description='type of the user, Patient or Doctor'
    )


class UserCreate(SQLModel):
    password: str = Field(nullable=True)
    user_name: str = Field(
        nullable=False, description='type of the user, Patient or Doctor'
    )


class UserUpdate(UserBase):
    password: str = Field(nullable=True)


class User(UserBase, table=True):
    __tablename__ = metadata.USER_TABLE
    __table_args__ = {'extend_existing': True, 'schema': metadata.SCHEMA_NAME}

    id: int = Field(default=None, primary_key=True)


class UserPublic(UserBase):
    id: int


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int
