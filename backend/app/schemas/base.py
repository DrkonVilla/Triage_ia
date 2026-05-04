from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, Generic, TypeVar, List
from pydantic.alias_generators import to_camel

T = TypeVar('T')

class BaseSchema(BaseModel):
    """Esquema base con configuración estándar"""
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
        arbitrary_types_allowed=True
    )

class ResponseModel(BaseSchema, Generic[T]):
    """Respuesta estándar de API"""
    success: bool = True
    data: Optional[T] = None
    message: Optional[str] = None
    errors: Optional[List[str]] = None

class PaginationParams(BaseSchema):
    """Parámetros de paginación"""
    page: int = Field(1, ge=1)
    per_page: int = Field(20, ge=1, le=100)
    sort_by: Optional[str] = None
    sort_desc: bool = False

class PaginatedResponse(BaseSchema, Generic[T]):
    """Respuesta paginada"""
    items: List[T]
    total: int
    page: int
    per_page: int
    pages: int