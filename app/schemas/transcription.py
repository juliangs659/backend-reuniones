from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, field_serializer
from bson import ObjectId


class TranscriptionCreate(BaseModel):
    """Schema para crear una transcripción"""
    transcription_text: str = Field(..., min_length=10)
    user_email: str = Field(..., description="Email del usuario")
    meeting_id: Optional[str] = None
    project_id: Optional[str] = None
    language: str = Field(default="es")
    source: str = Field(default="teams")


class TranscriptionUpdate(BaseModel):
    """Schema para actualizar una transcripción"""
    transcription_text: Optional[str] = None
    meeting_id: Optional[str] = None
    project_id: Optional[str] = None
    language: Optional[str] = None
    status: Optional[str] = None
    ai_analysis: Optional[Dict[str, Any]] = None


class TranscriptionResponse(BaseModel):
    """Schema de respuesta para transcripción"""
    id: Any = Field(alias="_id")
    transcription_text: str
    user_email: str
    meeting_id: Optional[Any] = None
    project_id: Optional[Any] = None
    language: str
    source: str
    status: str
    processed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    ai_analysis: Optional[Dict[str, Any]] = None
    ai_model_used: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @field_serializer('id', 'meeting_id', 'project_id')
    def serialize_object_id(self, value: Any) -> Optional[str]:
        if isinstance(value, ObjectId):
            return str(value)
        return value
    
    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True


class TranscriptionProcessRequest(BaseModel):
    """Schema para procesar transcripción con IA"""
    project_context: Optional[str] = Field(
        None,
        description="Contexto adicional del proyecto para mejorar el análisis"
    )
