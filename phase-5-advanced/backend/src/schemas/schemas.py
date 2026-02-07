from pydantic import BaseModel, EmailStr
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
    priority: str = "medium"        # NEW
    due_date: Optional[str] = None  # NEW


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None        # NEW
    due_date: Optional[str] = None        # NEW


class TaskResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    completed: bool
    priority: str                          # NEW
    due_date: Optional[str] = None         # NEW
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


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
