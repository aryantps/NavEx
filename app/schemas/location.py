from pydantic import BaseModel, Field, constr, conint, confloat
from typing import Optional
from datetime import datetime

class LocationBase(BaseModel):
    tenant: constr(min_length=1)
    user_id: Optional[constr(min_length=1)]

    location_code: constr(min_length=1, max_length=20)
    location_name: constr(min_length=1, max_length=100)

    latitude: confloat(ge=-90, le=90)
    longitude: confloat(ge=-180, le=180)

    city_name: constr(min_length=1, max_length=100)
    city_code: Optional[constr(max_length=10)]

    state_name: constr(min_length=1, max_length=100)
    state_code: Optional[constr(max_length=10)]

    district: Optional[str]
    taluka: Optional[str]
    zone: Optional[str]
    area_office: Optional[str]

    address: constr(min_length=1)
    pincode: constr(min_length=6, max_length=6)

    location_type: Optional[int]

    gps_radius: conint(gt=0) = 500
    sim_radius: conint(gt=0) = 5000
    avg_loading_time: Optional[int]

class LocationCreate(LocationBase):
    pass

class LocationRead(LocationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
