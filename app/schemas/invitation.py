from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class InvitationBase(BaseModel):
    email: EmailStr
    tenant_id: int


class InvitationCreate(InvitationBase):
    role_id: Optional[int] = None


class InvitationUpdate(BaseModel):
    status: Optional[str]  # expected: accepted, rejected


class InvitationRead(InvitationBase):
    id: int
    role_id: Optional[int]
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
