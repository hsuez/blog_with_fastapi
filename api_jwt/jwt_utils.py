from datetime import (
    timedelta,
    datetime,
    timezone,
)
from typing import Annotated

from database.database_utils import UserPydantic

import os
import jwt


TYPE_TOKEN: str = 'type'
TYPE_REFRESH_TOKEN: str ='refresh'
TYPE_ACCESS_TOKEN: str ='access'
EXP_ACCESS_TOKEN: int = 15  # 15 minutes
EXP_REFRESH_TOKEN: int = 30  # 30 days
algorithm: str = 'RS256'

def create_access_token(
    payload: UserPydantic,
    expires_delta: timedelta = timedelta(minutes=EXP_ACCESS_TOKEN),
    private_key_path: str = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'jwt_private.pem'),
):
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
    payload: UserPydantic,
    expires_delta: timedelta = timedelta(days=EXP_REFRESH_TOKEN),
    private_key_path: str = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'jwt_private.pem'),
):
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