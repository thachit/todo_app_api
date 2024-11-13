from urllib.request import Request

from fastapi import APIRouter, Depends
from typing import List, AnyStr
from src.schemas.register import RegisterDto
from src.schemas.users import UserResponse
from src.services.users.create_user import create_user
register_router_v1 = APIRouter(
    prefix="/register",
    tags=["register"]
)

@register_router_v1.post("", response_model=UserResponse)
async def register_user_api(params: RegisterDto):
    created_user = await create_user(params)
    return created_user