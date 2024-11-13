from fastapi import APIRouter
from src.schemas.login import LoginDto, LoginResponse
from src.services.auths.basic_login import basic_login

login_router_v1 = APIRouter(
    prefix="/login",
    tags=["login"]
)

@login_router_v1.post("", response_model=LoginResponse)
async def login_user_api(params: LoginDto):
    response = await basic_login(params)
    return response