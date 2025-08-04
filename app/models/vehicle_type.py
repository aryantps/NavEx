from pydantic import BaseModel, Field, confloat
from typing import Optional
from datetime import datetime
from enum import Enum


class VehicleTypeEnum(str, Enum):
    CAR = "car"
    TRUCK = "truck"
    VAN = "van"


class VehicleTypeBase(BaseModel):
    type: VehicleTypeEnum
    code: str = Field(..., max_length=80)
    tenant: str = Field(..., max_length=50)
    created_by: Optional[str] = Field(None, max_length=50)
    updated_by: Optional[str] = Field(None, max_length=50)
    is_active: bool = True
    length: confloat(gt=0)
    breadth: confloat(gt=0)
    height: confloat(gt=0)
    load_capacity: Optional[confloat(gt=0)] = None


class VehicleTypeCreate(VehicleTypeBase):
    pass


class VehicleTypeRead(VehicleTypeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True