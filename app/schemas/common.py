from typing import Optional, Any, Generic, TypeVar, List
from pydantic import BaseModel

T = TypeVar('T')


class Message(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    code: Optional[str] = None


class PaginationParams(BaseModel):
    skip: int = 0
    limit: int = 100


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    pages: int
