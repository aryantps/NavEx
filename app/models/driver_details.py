from pydantic import BaseModel, Field, constr, conbool
from typing import Optional
from datetime import datetime

class DriverDetailBase(BaseModel):
    tenant: constr(min_length=1)
    driver_name: constr(min_length=1)
    contact_number: Optional[str]
    driver_address: Optional[str]
    ext_driver_id: Optional[str]
    license_number: constr(min_length=1)
    license_expiry: Optional[datetime]
    license_issue: Optional[datetime]
    is_active: bool = True
    is_dedicated: bool = False
    is_assigned: bool = False
    pincode: Optional[constr(max_length=100)]
    location_code: Optional[str]
    location_name: Optional[str]

class DriverDetailCreate(DriverDetailBase):
    pass

class DriverDetailRead(DriverDetailBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True