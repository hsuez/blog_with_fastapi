from fastapi import APIRouter

from .registry_router import router as router_registry


router = APIRouter(prefix='/registration', tags=['registration'])
router.include_router(router_registry)