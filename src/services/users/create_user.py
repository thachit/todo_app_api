from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from src.db.db import get_session
from src.schemas.register import RegisterDto
from src.schemas.users import UserResponse
from src.models.user import User
from src.utils.hashing.encrypt import encrypt_password


async def create_user(params: RegisterDto) -> UserResponse:
    try:
        with get_session() as session:
            user = User(
                email=params.email,
                hashed_password=encrypt_password(params.password),
                username=params.username,
                full_name=params.full_name
            )
            session.add(user)
            session.commit()

            response = UserResponse(
                id=user.id,
                email=user.email,
                username=user.username,
                full_name=user.full_name,
                created_at=user.created_at
            )
            return response

    except IntegrityError as e:
        session.rollback()
        error_field = 'email' if 'email' in e.args[0] else 'username'
        raise HTTPException(detail=f"{error_field} is already registered", status_code=409)
    except Exception as e:
        session.rollback()
        raise HTTPException(detail=f"Internal Server Error", status_code=500)

