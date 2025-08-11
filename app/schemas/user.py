from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    tenant_id: Optional[int] = None

class UserCreate(UserBase):
    password: str  # assume hashed during creation

class UserUpdate(BaseModel):
    full_name: Optional[str]
    is_active: Optional[bool]
    password: Optional[str]

class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
