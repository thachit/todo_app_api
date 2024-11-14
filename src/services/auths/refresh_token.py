from src.schemas.token import RefreshTokenDto
from src.utils.jwt_token import exchange_refresh_token

async def refresh_token(
        params: RefreshTokenDto
):
    new_access_token, expires_in, new_refresh_token = exchange_refresh_token(params.refresh_token)
    return {
        "access_token": new_access_token,
        "token_type": "bearer",
        "expires_in": expires_in,
        "refresh_token": new_refresh_token
    }