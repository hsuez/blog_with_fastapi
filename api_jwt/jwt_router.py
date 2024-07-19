from fastapi import (
    APIRouter,
    # Form,
    Depends,
    Response,
)
from sqlalchemy.ext.asyncio import AsyncSession

from .auth import AuthUser, validate_auth_user
from .cookie_db import db_cookie
from .jwt_utils import (
    generate_session_id,
    create_access_token,
    create_refresh_token,
)
from .cookie_db.database_utils import Cookies
from .jwt_utils import User_name_email

COOKIE_SESSION_ID_KEY = 'session_id'

router = APIRouter()

@router.post('/')
async def auth_user(
    response: Response,
    user: AuthUser,
    session: AsyncSession = Depends(db_cookie.get_session)
):
    user_data = await validate_auth_user(
        user=user,
        session=session,
    )
    payload = User_name_email(username=user_data.username, email=user_data.email)
    session_id = generate_session_id()
    response.set_cookie(key=COOKIE_SESSION_ID_KEY, value=session_id)
    cookie_data = Cookies(
        session_id=session_id,
        access_token=create_access_token(payload=payload),
        refresh_token=create_refresh_token(payload=payload)
    )
    await db_cookie.create_cookie(session=session, cookies=cookie_data)
    return {
        'message': f'User {user.username} has been authenticated'
    }