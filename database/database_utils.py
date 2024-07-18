from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional

from config import settings
from . import User


class UserPydantic(BaseModel):
    username: str
    password: str
    email: Optional[str] = None

class DataBase:
    def __init__(self):
        self.engine = create_async_engine(
            url=settings.DATABASE_URI,
            echo=True,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False,
        )

    @staticmethod
    async def insert_user(
        user_in: UserPydantic,
        session: AsyncSession,
    ):
        async with session() as session:
            async with session.begin():
                user = User(**user_in.model_dump())
                session.add(user)
                await session.commit()
                return {
                    'message': f'User {user.username} has been registered'
                }
            
    @staticmethod
    async def get_users(
        session: AsyncSession,
    ):
        query = select(User).order_by('users.id')
        result = await session.execute(query)
        return result.scalars().all()

db = DataBase()