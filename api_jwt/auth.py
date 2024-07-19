from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from database import db

import bcrypt


class AuthUser(BaseModel):
    username: str
    password: str


def validate_password(
    password_hash_from_db: str,
    password_user: str,
):
    print(f'{password_user}: {type(password_user)}')
    print(f'{password_hash_from_db}: {type(password_hash_from_db)}')
    password = password_user.encode()
    return bcrypt.checkpw(password, password_hash_from_db)



async def validate_auth_user(
    user: AuthUser,
    session: AsyncSession,
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Incorrect username or password',
    )

    user_from_db = await db.get_user_by_username(
        username=user.username,
        session=session,
    )
    
    if user_from_db is None:
        raise unauthed_exc
    
    if not validate_password(
        password_hash_from_db = user_from_db.password_hash,
        password_user = user.password,
    ):
        raise unauthed_exc
    
    return user_from_db