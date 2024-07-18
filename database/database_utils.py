from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncEngine,
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
        self.engine: AsyncEngine = create_async_engine(
            url=settings.DATABASE_URI,
            echo=True,
        )

    def get_session(self):
        self.session_factory: AsyncSession = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False,
        )
        return self.session_factory()

    @staticmethod
    async def insert_user(
        user_in: UserPydantic,
        session: AsyncSession,
    ):
        # async with session() as session:
        async with session.begin():
            user = User(
                username=user_in.username,
                password_hash=user_in.password,
                email=user_in.email,
            )
            session.add(user)
            await session.commit()
            return {
                'message': f'User {user.username} has been registered'
            }
            
    # @sAsyncSession,
    # ):taticmethod
    # async def get_users(
    #     session: 
    #     query = select(User).order_by('users.id')
    #     result = await session.execute(query)
    #     return result.scalars().all()
    
    @staticmethod
    async def get_user_by_username(
        username: str,
        session: AsyncSession,
    ):
        async with session.begin():
            query = select(User).filter_by(username=username)
            result = await session.execute(query)
            return result.scalars().first()

db = DataBase()