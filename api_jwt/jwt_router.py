from fastapi import (
    APIRouter,
    Depends,
    Response,
    Cookie,
    HTTPException,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession
from .auth import AuthUser, validate_auth_user
from .jwt_utils import (
    generate_session_id,
    create_access_token,
    create_refresh_token,
    validate_access_token,
)
from .jwt_utils import User_name_email
from database.database_utils import CookiePydantic, db


COOKIE_SESSION_ID_KEY = 'session_id'

router = APIRouter()

@router.post('/')
async def auth_user(
    response: Response,
    user: AuthUser,
    session: AsyncSession = Depends(db.get_session)
):
    user_data = await validate_auth_user(
        user=user,
        session=session,
    )
    payload = User_name_email(username=user_data.username, email=user_data.email)
    session_id = generate_session_id()
    response.set_cookie(key=COOKIE_SESSION_ID_KEY, value=session_id)
    cookie_data = CookiePydantic(
        session_id=session_id,
        access_token=create_access_token(payload=payload),
        refresh_token=create_refresh_token(payload=payload),
    )
    await db.create_cookie(session=session, cookie=cookie_data)
    return {
        'message': f'User {user.username} has been authenticated'
    }

async def get_session_data(
    session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY),
    session: AsyncSession = Depends(db.get_session)
):
    if session_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Missing session ID cookie'
        )
    return await validate_access_token(
        session=session,
        session_id=session_id,
    )

@router.get('/authorization/')
async def authorization_user(
    session_data: dict = Depends(get_session_data),
):
    return await session_data()