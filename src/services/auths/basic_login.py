from fastapi import HTTPException
from src.schemas.login import LoginDto
from src.schemas.token import TokenResponse
from src.db.db import get_session
from src.models.user import User
from src.utils.hashing.encrypt import check_password
from src.utils.jwt_token import create_jwt_token

async def basic_login(params: LoginDto) -> TokenResponse:

    with get_session() as session:
        user = session.query(User).filter(User.email == params.email).first()
        if not user:
            raise HTTPException(detail="Invalid email or password", status_code=401)

    is_password_valid = check_password(params.password, user.hashed_password)
    if not is_password_valid:
        raise HTTPException(detail="Invalid email or password", status_code=401)

    access_token, expires_in = create_jwt_token(user.id, user.username, is_refresh=False)
    refresh_token, refresh_expires_in = create_jwt_token(user.id, user.username, is_refresh=True)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": expires_in,
        "refresh_token": refresh_token
    }

