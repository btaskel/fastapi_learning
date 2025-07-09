from fastapi import FastAPI

from src.router.user import router

app = FastAPI()

app.include_router(router)