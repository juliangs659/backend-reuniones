from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, validator
from app.schemas.meeting import MeetingSummary
from app.schemas.user import UserProfile


class TranscriptionBase(BaseModel):
    """Esquema base para transcripción"""
    title: Optional[str] = None
    original_language: Optional[str] = "es"
    is_sensitive: Optional[bool] = False
    retention_days: Optional[int] = 365
    processing_options: Optional[Dict[str, Any]] = None
    
    @validator('retention_days')
    def validate_retention_days(cls, v):
        if v is not None and (v < 1 or v > 3650):  # máximo 10 años
            raise ValueError('Retention days debe estar entre 1 y 3650')
        return v


class TranscriptionCreate(TranscriptionBase):
    """Esquema para crear transcripción"""
    meeting_id: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "meeting_id": 1,
                "title": "Transcripción - Revisión de Progreso",
                "original_language": "es",
                "is_sensitive": False,
                "retention_days": 365,
                "processing_options": {
                    "model": "whisper-1",
                    "temperature": 0.2,
                    "enable_speaker_detection": True,
                    "enable_summary": True,
                    "enable_key_points": True
                }
            }
        }


class TranscriptionUpdate(TranscriptionBase):
    """Esquema para actualizar transcripción"""
    transcript_text: Optional[str] = None
    summary: Optional[str] = None
    key_points: Optional[List[str]] = None
    commitments: Optional[List[str]] = None
    next_steps: Optional[List[str]] = None
    participants: Optional[List[str]] = None
    processing_status: Optional[str] = None
    confidence_score: Optional[float] = None
    ai_model_used: Optional[str] = None
    error_message: Optional[str] = None
    processing_logs: Optional[List[Dict[str, Any]]] = None
    
    @validator('processing_status')
    def validate_processing_status(cls, v):
        if v is not None:
            allowed_statuses = ['pending', 'processing', 'completed', 'failed']
            if v not in allowed_statuses:
                raise ValueError(f'Processing status debe ser uno de: {", ".join(allowed_statuses)}')
        return v
    
    @validator('confidence_score')
    def validate_confidence_score(cls, v):
        if v is not None and (v < 0.0 or v > 1.0):
            raise ValueError('Confidence score debe estar entre 0.0 y 1.0')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "transcript_text": "Buenos días a todos. Hoy vamos a revisar el progreso del proyecto...",
                "summary": "Reunión de seguimiento donde se revisó el progreso del rediseño web.",
                "key_points": [
                    "El diseño está 75% completado",
                    "Se necesita feedback del cliente",
                    "Próxima entrega el viernes"
                ],
                "commitments": [
                    "Juan enviará mockups actualizados",
                    "María contactará al cliente para feedback"
                ],
                "next_steps": [
                    "Revisar feedback del cliente",
                    "Implementar cambios solicitados",
                    "Preparar presentación final"
                ],
                "participants": ["Juan Pérez", "María García", "Carlos López"],
                "processing_status": "completed",
                "confidence_score": 0.95
            }
        }


class TranscriptionInDBBase(TranscriptionBase):
    """Esquema base para transcripción en base de datos"""
    id: int
    transcript_text: Optional[str] = None
    summary: Optional[str] = None
    key_points: Optional[List[str]] = None
    commitments: Optional[List[str]] = None
    next_steps: Optional[List[str]] = None
    participants: Optional[List[str]] = None
    audio_filename: Optional[str] = None
    audio_duration_seconds: Optional[int] = None
    audio_format: Optional[str] = None
    audio_size_bytes: Optional[int] = None
    processing_status: str
    confidence_score: Optional[float] = None
    processing_started_at: Optional[datetime] = None
    processing_completed_at: Optional[datetime] = None
    ai_model_used: Optional[str] = None
    error_message: Optional[str] = None
    processing_logs: Optional[List[Dict[str, Any]]] = None
    meeting_id: int
    processed_by_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class Transcription(TranscriptionInDBBase):
    """Esquema para transcripción (respuesta)"""
    meeting: Optional[MeetingSummary] = None
    processed_by: Optional[UserProfile] = None
    is_completed: Optional[bool] = None
    is_failed: Optional[bool] = None
    processing_duration_seconds: Optional[float] = None
    word_count: Optional[int] = None
    should_be_deleted: Optional[bool] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Transcripción - Revisión de Progreso",
                "transcript_text": "Buenos días a todos. Hoy vamos a revisar...",
                "summary": "Reunión de seguimiento del proyecto de rediseño web.",
                "key_points": [
                    "Progreso del 75% completado",
                    "Feedback del cliente pendiente"
                ],
                "commitments": [
                    "Juan enviará mockups actualizados"
                ],
                "next_steps": [
                    "Revisar feedback del cliente"
                ],
                "participants": ["Juan Pérez", "María García"],
                "audio_filename": "meeting-recording-123.mp3",
                "audio_duration_seconds": 3600,
                "audio_format": "mp3",
                "audio_size_bytes": 25600000,
                "processing_status": "completed",
                "confidence_score": 0.95,
                "processing_started_at": "2024-02-15T11:05:00Z",
                "processing_completed_at": "2024-02-15T11:15:00Z",
                "ai_model_used": "whisper-1",
                "original_language": "es",
                "is_sensitive": False,
                "retention_days": 365,
                "meeting_id": 1,
                "processed_by_id": 1,
                "is_completed": True,
                "is_failed": False,
                "processing_duration_seconds": 600.0,
                "word_count": 1250,
                "should_be_deleted": False,
                "created_at": "2024-02-15T11:05:00Z",
                "updated_at": "2024-02-15T11:15:00Z"
            }
        }


class TranscriptionInDB(TranscriptionInDBBase):
    """Esquema para transcripción en base de datos (con campos internos)"""
    pass


class TranscriptionSummary(BaseModel):
    """Esquema para resumen de transcripción"""
    id: int
    title: Optional[str] = None
    processing_status: str
    confidence_score: Optional[float] = None
    word_count: Optional[int] = None
    meeting_title: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Transcripción - Revisión de Progreso",
                "processing_status": "completed",
                "confidence_score": 0.95,
                "word_count": 1250,
                "meeting_title": "Revisión de Progreso - Rediseño Web",
                "created_at": "2024-02-15T11:05:00Z"
            }
        }


class AudioUploadRequest(BaseModel):
    """Esquema para solicitud de subida de audio"""
    meeting_id: int
    processing_options: Optional[Dict[str, Any]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "meeting_id": 1,
                "processing_options": {
                    "model": "whisper-1",
                    "temperature": 0.2,
                    "enable_speaker_detection": True,
                    "enable_summary": True
                }
            }
        }


class AudioUploadResponse(BaseModel):
    """Esquema para respuesta de subida de audio"""
    transcription_id: int
    message: str
    processing_status: str
    estimated_completion_time: Optional[datetime] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "transcription_id": 1,
                "message": "Audio subido exitosamente. Procesamiento iniciado.",
                "processing_status": "processing",
                "estimated_completion_time": "2024-02-15T11:20:00Z"
            }
        }


class TranscriptionRegenerateRequest(BaseModel):
    """Esquema para solicitud de regenerar resumen"""
    include_summary: Optional[bool] = True
    include_key_points: Optional[bool] = True
    include_commitments: Optional[bool] = True
    include_next_steps: Optional[bool] = True
    custom_prompt: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "include_summary": True,
                "include_key_points": True,
                "include_commitments": True,
                "include_next_steps": True,
                "custom_prompt": "Enfócate en los aspectos técnicos del proyecto"
            }
        }