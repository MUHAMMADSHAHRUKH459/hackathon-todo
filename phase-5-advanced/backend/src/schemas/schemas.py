from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional

# --------------------
# User Schemas
# --------------------

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


# --------------------
# Task Schemas
# --------------------

class TaskCreate(BaseModel):
    title: str
    description: str = ""
    priority: str = "medium"
    due_date: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    due_date: Optional[str] = None


class TaskResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    completed: bool
    priority: str
    due_date: Optional[str] = None
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }

    @field_validator('created_at', 'updated_at', 'due_date', mode='before')
    @classmethod
    def datetime_to_str(cls, v):
        if isinstance(v, datetime):
            return v.isoformat()
        return v


# --------------------
# Auth Schemas
# --------------------

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


class LoginRequest(BaseModel):
    username: str
    password: str