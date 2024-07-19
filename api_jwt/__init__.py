from fastapi import APIRouter

from .jwt_router import router as auth_jwt_router


router = APIRouter(prefix='/auth', tags=['auth'])
router.include_router(auth_jwt_router)