from pydantic import BaseModel, Field, constr, conint, confloat
from typing import Optional
from datetime import datetime

class TripBase(BaseModel):
    trip_code: constr(min_length=1, max_length=100)
    status: constr(min_length=1, max_length=100)

    trip_start_time: Optional[datetime]
    trip_end_time: Optional[datetime]

    origin_name: constr(min_length=1, max_length=100)
    destination_name: constr(min_length=1, max_length=100)

    vehicle_code: constr(min_length=1, max_length=100)
    vehicle_number: constr(min_length=1, max_length=50)

    total_distance: Optional[float]
    total_trip_kms: float = 0
    total_time: Optional[float]
    tat: Optional[int]

    driver_name: Optional[str]
    driver_number: Optional[str]

    started_by: Optional[str]
    stopped_by: Optional[str]
    created_by: Optional[str]
    updated_by: Optional[str]

    client_name: Optional[str]
    driver_consent_status: Optional[str]
    shipment_codes: Optional[str]
    comments: Optional[str]

    tenant: constr(min_length=1)

class TripCreate(TripBase):
    pass

class TripRead(TripBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }