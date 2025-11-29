from typing import Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field, field_serializer
from bson import ObjectId


class ProjectPhaseCreate(BaseModel):
    """Schema para crear fase de proyecto"""
    project_id: str
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    order: int = Field(..., ge=1)
    status: str = Field(default="pending")
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class ProjectPhaseUpdate(BaseModel):
    """Schema para actualizar fase"""
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    order: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    actual_start_date: Optional[datetime] = None
    actual_end_date: Optional[datetime] = None
    completion_percentage: Optional[int] = Field(None, ge=0, le=100)


class ProjectPhaseResponse(BaseModel):
    """Schema de respuesta para fase"""
    id: Any = Field(alias="_id")
    project_id: Any
    name: str
    description: Optional[str] = None
    status: str
    order: int
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    actual_start_date: Optional[datetime] = None
    actual_end_date: Optional[datetime] = None
    completion_percentage: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @field_serializer('id', 'project_id')
    def serialize_object_id(self, value: Any) -> Optional[str]:
        return str(value) if isinstance(value, ObjectId) else value
    
    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True


class PhaseReorderItem(BaseModel):
    """Item individual para reordenar"""
    phase_id: str
    order: int


class PhaseReorderRequest(BaseModel):
    """Schema para reordenar fases"""
    phase_orders: list[PhaseReorderItem] = Field(
        ...,
        description="Lista de fases con su nuevo orden"
    )
