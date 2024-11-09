from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class UserResponse(BaseModel):
    id: Optional[int]
    username: Optional[str]
    email: Optional[str]
    full_name: Optional[str]
    created_at: Optional[datetime]