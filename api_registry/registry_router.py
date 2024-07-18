from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

import bcrypt

from database import UserPydantic as UserIn
from database import db
from .validation import validate_credentials


router = APIRouter()

def generate_password_hash(password):
    salt = bcrypt.gensalt()
    password = password.encode()
    return bcrypt.hashpw(password, salt)


@router.post('/')
async def register_user(
    user: UserIn,
    session: AsyncSession = Depends(db.get_session)
):
    exc = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='User with this username already exists'
    )
    password_hash = generate_password_hash(user.password)
    if not validate_credentials(user):
        raise exc
    return await db.insert_user(
        UserIn(username=user.username, password=password_hash),
        session=session,
    )