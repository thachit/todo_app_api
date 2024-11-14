from fastapi import APIRouter
from src.schemas.token import TokenResponse, RefreshTokenDto
from src.services.auths.refresh_token import refresh_token

refresh_token_router_v1 = APIRouter(
    prefix="/refresh-token",
    tags=["refresh-token"]
)

@refresh_token_router_v1.post("", response_model=TokenResponse)
async def refresh_token_api(params: RefreshTokenDto):
    response = await refresh_token(params)
    return response