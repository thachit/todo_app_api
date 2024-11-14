from pydantic import BaseModel, field_validator, EmailStr, Field


class BaseLoginDto(BaseModel):
    email: EmailStr = Field(max_length=100)


class LoginDto(BaseLoginDto):
    password: str = Field()

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