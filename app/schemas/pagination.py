from pydantic import BaseModel, Field
from typing import  Generic, List, Optional, TypeVar

class PaginatedQueryRequest(BaseModel):
    page: int = Field(1, ge=1, description="Page number (1-indexed)")
    page_size: int = Field(10, ge=1, le=100, description="Number of items per page")
    order_by: Optional[str] = Field("id", description="Field to order by")
    order_direction: Optional[str] = Field("ASC", pattern="^(ASC|DESC)$", description="Order direction: ASC or DESC")

ModelType = TypeVar("ModelType)")

class Pagination(BaseModel):
    page: int
    size: int
    count: int
    next: Optional[int]
    previous: Optional[int]

class PaginatedQueryResponse(BaseModel, Generic[ModelType]):
    results: List[ModelType]
    pagination: Pagination
