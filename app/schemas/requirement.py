from typing import Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field, field_serializer
from bson import ObjectId


class RequirementCreate(BaseModel):
    """Schema para crear requerimiento"""
    project_id: str
    phase_id: str
    transcription_id: Optional[str] = None
    title: str = Field(..., min_length=1)
    description: str
    type: str = Field(default="functional")
    priority: str = Field(default="medium")
    status: str = Field(default="pending")


class RequirementUpdate(BaseModel):
    """Schema para actualizar requerimiento"""
    phase_id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    user_edited: Optional[bool] = None


class RequirementResponse(BaseModel):
    """Schema de respuesta para requerimiento"""
    id: Any = Field(alias="_id")
    project_id: Any
    phase_id: Any
    transcription_id: Optional[Any] = None
    title: str
    description: str
    type: str
    priority: str
    status: str
    extracted_by_ai: bool
    user_edited: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @field_serializer('id', 'project_id', 'phase_id', 'transcription_id')
    def serialize_object_id(self, value: Any) -> Optional[str]:
        return str(value) if isinstance(value, ObjectId) else value
    
    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True
