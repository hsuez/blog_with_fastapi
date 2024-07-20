from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncEngine,
)
from sqlalchemy import select, update, delete
from pydantic import BaseModel
from typing import Optional, Union

from db_config.config import settings
from . import User, Cookie


class UserPydantic(BaseModel):
    username: str
    password: Union[str, bytes]
    email: Optional[str] = None

class CookiePydantic(BaseModel):
    session_id: str
    access_token: str
    refresh_token: str

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
        return self.session_factory

    # interaction with users database
    @staticmethod
    async def insert_user(
        user_in: UserPydantic,
        session: AsyncSession,
    ):
        async with session() as session:
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
            
    @staticmethod
    async def get_user_by_username(
        username: str,
        session: AsyncSession,
    ):
        async with session() as session:
            query = select(User).filter_by(username=username)
            result = await session.execute(query)
            return result.scalars().first()
        
    # interaction with cookies database
    @staticmethod
    async def create_cookie(
        session: AsyncSession,
        cookie: CookiePydantic,
    ):
        async with session() as session:
            cookie = Cookie(**cookie.model_dump())
            session.add(cookie)
            await session.commit()
            
    @staticmethod
    async def get_cookie_by_session_id(
        session_id: str,
        session: AsyncSession,
    ):
        async with session() as session:
            query = select(Cookie).filter_by(session_id=session_id)
            result = await session.execute(query)
            return result.scalars().first()
        
    @staticmethod
    async def update_access_token(
        session: AsyncSession,
        access_token: str,
        session_id: str,
    ):
        async with session() as session:
            stmt = update(Cookie).filter_by(session_id=session_id).values(access_token=access_token)
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def delete_cookie(
        session: AsyncSession,
        session_id: str,
    ):
        async with session() as session:
            stmt = delete(Cookie).filter_by(session_id=session_id)
            await session.execute(stmt)
            await session.commit()


db = DataBase()