from fastapi import FastAPI

from api_registry import router as registry_router
from api_jwt import router as auth_jwt_router


app = FastAPI()
app.include_router(registry_router)
app.include_router(auth_jwt_router)