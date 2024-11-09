from typing import Optional
from pydantic import BaseModel, Field, EmailStr, field_validator

class RegisterDto(BaseModel):
    email: EmailStr = Field(max_length=100)
    password: str = Field()
    username: str = Field(max_length=32)
    full_name: Optional[str] = Field(max_length=160)

    @field_validator('password')
    def validate_password(password):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.islower() for c in password):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isupper() for c in password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in password):
            raise ValueError("Password must contain at least one digit")

        return password

