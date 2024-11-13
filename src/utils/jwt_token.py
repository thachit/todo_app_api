import jwt
import datetime
from src.core.config import Config

SECRET = Config.SECRET_KEY
EXPIRED_TIME = Config.TOKEN_EXPIRATION

def create_jwt_token(user_id: int, username: str) -> str:
    payload = {
        "iss": Config.APP_NAME,
        "sub": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=EXPIRED_TIME),
        "iat": datetime.datetime.utcnow(),
        "userId": user_id,
    }

    token = jwt.encode(payload, SECRET, algorithm="HS256")
    return token, EXPIRED_TIME