from fastapi import APIRouter
from src.schemas.login import LoginDto
from src.schemas.token import TokenResponse
from src.services.auths.basic_login import basic_login

login_router_v1 = APIRouter(
    prefix="/login",
    tags=["login"]
)

@login_router_v1.post("", response_model=TokenResponse)
async def login_user_api(params: LoginDto):
    response = await basic_login(params)
    return response