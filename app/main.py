from fastapi import FastAPI
from app.api.endpoints import router
from app.core.logging_config import setup_logging

app = FastAPI()
app.include_router(router)

setup_logging()