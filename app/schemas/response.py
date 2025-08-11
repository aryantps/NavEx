from pydantic import BaseModel
from typing import Generic, Optional, TypeVar

DataType = TypeVar("DataType")

class APIResponse(BaseModel, Generic[DataType]):
    success: bool
    code: int
    message: Optional[str] = None
    data: Optional[DataType] = None
