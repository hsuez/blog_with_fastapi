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
    get_tokens_from_db,
    COOKIE_SESSION_ID_KEY,
    decoded_token,
    User_name_email,
)
from .jwt_utils import User_name_email
from database.database_utils import CookiePydantic, db


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

@router.get('/authorization/')
async def authorization_user(
    response: Response,
    session: AsyncSession = Depends(db.get_session),
    session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY)
):
    if session_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Missing session ID cookie',
        )
    try:
        tokens = await get_tokens_from_db(
            session=session,
            session_id=session_id,
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='You dont authenticate',
        )
    # return dict : {session_id, access_token, refresh_token}
    try:
        access_payload = decoded_token(token=tokens['access_token'])
        return access_payload
    except:
        try:
            # update access token in db if has refresh token
            refresh_payload = decoded_token(token=tokens['refresh_token'])
            new_access_token = create_access_token(
                payload=User_name_email(username=refresh_payload['sub'], email=refresh_payload['email']),
            )
            await db.update_access_token(
                session=session,
                access_token=new_access_token,
                session_id=session_id,
            )
            return {
                'message': 'Update access token',
                'token': new_access_token,
            }
        except:
            # delete cookies from db and from cookie
            await db.delete_cookie(
                session=session,
                session_id=session_id,
            )
            response.delete_cookie(key=COOKIE_SESSION_ID_KEY)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid access or refresh token',
            )