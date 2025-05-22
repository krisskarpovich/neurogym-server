from pydantic import BaseModel, EmailStr, Field, root_validator
from typing import Optional
from datetime import date


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    confirm_password: str
    weight: Optional[float] = None
    height: Optional[float] = None
    birth_date: Optional[date] = None

    @root_validator(skip_on_failure=True)
    def check_passwords_match(cls, values):
        pw = values.get("password")
        cpw = values.get("confirm_password")
        if pw != cpw:
            raise ValueError("Passwords do not match")
        return values

    # schemas.py

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class UserResponse(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    bmi: float

    class Config:
        orm_mode = True
