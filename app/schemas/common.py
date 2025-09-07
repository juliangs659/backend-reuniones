from typing import Optional, Any
from pydantic import BaseModel


class Message(BaseModel):
    """Esquema para mensajes de respuesta simples"""
    message: str
    

 class Config:
        json_schema_extra = {
            "example": {
                "message": "Operación completada exitosamente"
            }
        }


class ErrorResponse(BaseModel):
    """Esquema para respuestas de error"""
    error: str
    detail: Optional[str] = None
    code: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "Error de validación",
                "detail": "El campo 'email' es requerido",
                "code": "VALIDATION_ERROR"
            }
        }


class PaginationParams(BaseModel):
    """Parámetros de paginación"""
    skip: int = 0
    limit: int = 100
    
    class Config:
        json_schema_extra = {
            "example": {
                "skip": 0,
                "limit": 20
            }
        }


class PaginatedResponse(BaseModel):
    """Respuesta paginada genérica"""
    items: list[Any]
    total: int
    skip: int
    limit: int
    has_next: bool
    has_prev: bool
    
    class Config:
        json_schema_extra = {
            "example": {
                "items": [],
                "total": 100,
                "skip": 0,
                "limit": 20,
                "has_next": True,
                "has_prev": False
            }
        }