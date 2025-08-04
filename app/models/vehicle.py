from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime



class VehicleBase(BaseModel):
    vehicle_number: str = Field(..., max_length=50)
    vehicle_type_id: int
    is_assigned: bool = False
    tenant: str = Field(..., max_length=50)
    created_by: Optional[str] = Field(None, max_length=50)
    updated_by: Optional[str] = Field(None, max_length=50)
    vehicle_code: str = Field(..., max_length=100)
    tracking_asset_id: Optional[int] = None
    rc_number: Optional[str] = Field(None, max_length=100)
    puc_number: Optional[str] = Field(None, max_length=100)


class VehicleCreate(VehicleBase):
    pass


class VehicleRead(VehicleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
