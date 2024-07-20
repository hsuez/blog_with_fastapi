from fastapi import Cookie, HTTPException, status
from datetime import (
    timedelta,
    datetime,
    timezone,
)
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, Optional
from pydantic import BaseModel

from database.database_utils import UserPydantic, db

import os
import jwt
import uuid


class User_name_email(BaseModel):
    username: str
    email: Optional[str] = None


COOKIE_SESSION_ID_KEY = 'session_id'
TYPE_TOKEN: str = 'type'
TYPE_REFRESH_TOKEN: str ='refresh'
TYPE_ACCESS_TOKEN: str ='access'
EXP_ACCESS_TOKEN: int = 10  # 15 minutes
EXP_REFRESH_TOKEN: int = 30  # 30 days
algorithm: str = 'RS256'

def generate_session_id() -> str:
    return uuid.uuid4().hex


def create_access_token(
    payload: User_name_email,
    expires_delta: timedelta = timedelta(seconds=EXP_ACCESS_TOKEN),
    private_key_path: str = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'jwt_private.pem'),
) -> str:
    with open(private_key_path, 'r') as f:
        private_key = f.read()

    payload = {
        TYPE_TOKEN: TYPE_ACCESS_TOKEN, 
        'sub': payload.username,
        'iat': datetime.now(timezone.utc),
        'exp': datetime.now(timezone.utc) + expires_delta,
    }
    encoded = jwt.encode(payload=payload, key=private_key, algorithm=algorithm)
    return encoded


def create_refresh_token(
    payload: User_name_email,
    expires_delta: timedelta = timedelta(seconds=EXP_REFRESH_TOKEN),
    private_key_path: str = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'jwt_private.pem'),
) -> str:
    with open(private_key_path, 'r') as f:
        private_key = f.read()

    payload = {
        TYPE_TOKEN: TYPE_REFRESH_TOKEN, 
        'sub': payload.username,
        'email': payload.email,
        'exp': datetime.now(timezone.utc) + expires_delta,
        'iat': datetime.now(timezone.utc),
    }
    encoded = jwt.encode(payload=payload, key=private_key, algorithm=algorithm)
    return encoded

async def get_tokens_from_db(
    session: AsyncSession,
    session_id: str,
) -> dict:
    cookie_from_db = await db.get_cookie_by_session_id(
        session_id=session_id,
        session=session
    )
    return {
        'session_id': cookie_from_db.session_id,
        'access_token': cookie_from_db.access_token,
        'refresh_token': cookie_from_db.refresh_token,
    }

def decoded_token(
    token: str,
    public_key_path: str = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'jwt_public.pem'),
    algorithm: str = algorithm
) -> dict:
    with open(public_key_path , 'r') as f:
        public_key = f.read()
    # using with try-except constructor
    payload = jwt.decode(jwt=token, key=public_key, algorithms=[algorithm])
    return payload