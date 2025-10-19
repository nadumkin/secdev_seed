from pydantic import BaseModel, Field, validator
from typing import Optional


class LoginRequest(BaseModel):

    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=100)

    @validator('username')
    def validate_username(cls, v):
        if not v.isalnum():  # Только буквы и цифры для имени пользователя
            raise ValueError('Username must be alphanumeric')
        return v

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        return v

class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
