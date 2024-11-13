from sys import prefix

from fastapi import FastAPI
from src.core.config import Config
from src.api.api_v1.registers import register_router_v1
from src.api.api_v1.login import login_router_v1
fast_api = FastAPI()

# API V1
fast_api.include_router(register_router_v1, prefix='/api/v1')
fast_api.include_router(login_router_v1, prefix='/api/v1')
@fast_api.get("/health")
async def health_check():
    return {
        "status": "ok",
        "app_name": Config.APP_NAME
    }