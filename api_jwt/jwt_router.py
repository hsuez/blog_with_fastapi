from fastapi import (
    APIRouter,
    Form,
    Depends,
)
from sqlalchemy.ext.asyncio import AsyncSession

from .auth import AuthUser, validate_auth_user
from database import db


router = APIRouter()

@router.post('/')
async def auth_user(
    user: AuthUser = Form(),
    session: AsyncSession = Depends(db.get_session)
):
    validate_auth_user(
        user=user,
        session=session,
    )
    