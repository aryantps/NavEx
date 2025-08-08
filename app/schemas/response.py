from pydantic import BaseModel
from typing import Generic, Optional, TypeVar
from pydantic.generics import GenericModel

DataType = TypeVar("DataType")

class APIResponse(GenericModel, Generic[DataType]):
    success: bool
    code: int
    message: Optional[str] = None
    data: Optional[DataType] = None
