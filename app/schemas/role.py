from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class RoleBase(BaseModel):
    name: str
    tenant_id: int


class RoleCreate(RoleBase):
    pass


class RoleUpdate(BaseModel):
    name: Optional[str] = None


class RoleRead(RoleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
