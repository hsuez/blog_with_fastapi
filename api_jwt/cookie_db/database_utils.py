from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncEngine,
)
from pydantic import BaseModel

from . import settings, Cookie


class Cookies(BaseModel):
    session_id: str
    access_token: str
    refresh_token: str


class DataBaseCookies:
    def __init__(self):
        self.engine: AsyncEngine = create_async_engine(
            url=settings.DATABASE_URI,
            echo=True,
        )

    def get_session(self):
        self.session_factory: AsyncSession = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )
        return self.session_factory()
    
    @staticmethod
    async def create_cookie(
        session: AsyncSession,
        cookies: Cookies,
    ):
        async with session.begin():
            cookie = Cookie(**cookies.model_dump())
            session.add(cookie)
            await session.commit()
            return {
                'message': 'Created cookie'
            }
        
db_cookie = DataBaseCookies()