from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserRoleBase(BaseModel):
    user_id: int
    role_id: int
    tenant_id: int

class UserRoleCreate(UserRoleBase):
    pass

class UserRoleRead(UserRoleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
