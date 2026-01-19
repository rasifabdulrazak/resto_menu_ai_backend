from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel

T = TypeVar("T")


class ErrorSchema(BaseModel):
    code: str
    details: Optional[Any] = None


class MetaSchema(BaseModel):
    page: Optional[int] = None
    page_size: Optional[int] = None
    total: Optional[int] = None


class APIResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: Optional[T] = None
    meta: Optional[MetaSchema] = None
    errors: Optional[ErrorSchema] = None
