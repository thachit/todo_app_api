from fastapi import HTTPException
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError, InvalidTokenError
import datetime
from src.core.config import Config


ALGORITHM = "HS256"

def create_jwt_token(user_id: int, username: str, is_refresh: bool = False) -> str:
    payload = {
        "iss": Config.APP_NAME,
        "sub": username,
        "iat": datetime.datetime.utcnow(),
        "userId": user_id,
    }

    if is_refresh:
        expired_time = Config.REFRESH_TOKEN_EXPIRATION
        secret = Config.REFRESH_SECRET_KEY
    else:
        expired_time = Config.TOKEN_EXPIRATION
        secret = Config.SECRET_KEY

    payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(seconds=int(expired_time))

    token = jwt.encode(payload, secret, algorithm=ALGORITHM)
    return token, expired_time


def verify_jwt_token(refresh_token: str) -> str:
    try:
        decoded_payload = jwt.decode(
            jwt=refresh_token,
            key=Config.REFRESH_SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_exp": True}
        )
        return decoded_payload
    except Exception as e:
        raise HTTPException(detail="Token has expired or invalid", status_code=401)


def exchange_refresh_token(refresh_token: str) -> str:
    decoded_payload = verify_jwt_token(refresh_token)
    user_id = decoded_payload.get("userId")
    username = decoded_payload.get("sub")

    access_token, expires_in = create_jwt_token(user_id, username, is_refresh=False)
    refresh_token, refresh_expires_in = create_jwt_token(user_id, username, is_refresh=True)

    return access_token, expires_in, refresh_token