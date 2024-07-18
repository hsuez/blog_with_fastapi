from fastapi import FastAPI

from api_registry import router


app = FastAPI()
app.include_router(router)