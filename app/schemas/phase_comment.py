from typing import Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field, field_serializer
from bson import ObjectId


class PhaseCommentCreate(BaseModel):
    """Schema para crear comentario en fase"""
    phase_id: str
    project_id: str
    user_email: str
    comment: str = Field(..., min_length=1)
    is_internal: bool = Field(default=False)


class PhaseCommentUpdate(BaseModel):
    """Schema para actualizar comentario"""
    comment: Optional[str] = None
    is_internal: Optional[bool] = None


class PhaseCommentResponse(BaseModel):
    """Schema de respuesta para comentario"""
    id: Any = Field(alias="_id")
    phase_id: Any
    project_id: Any
    user_email: str
    comment: str
    is_internal: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @field_serializer('id', 'phase_id', 'project_id')
    def serialize_object_id(self, value: Any) -> Optional[str]:
        return str(value) if isinstance(value, ObjectId) else value
    
    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True
