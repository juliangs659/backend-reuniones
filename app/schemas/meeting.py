from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, validator
from app.schemas.project import ProjectSummary
from app.schemas.user import UserProfile


class MeetingBase(BaseModel):
    """Esquema base para reunión"""
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    password: Optional[str] = None
    is_recording_enabled: Optional[bool] = True
    max_participants: Optional[int] = 50
    require_password: Optional[bool] = False
    waiting_room_enabled: Optional[bool] = False
    meeting_notes: Optional[str] = None
    jitsi_config: Optional[Dict[str, Any]] = None
    
    @validator('max_participants')
    def validate_max_participants(cls, v):
        if v is not None and (v < 1 or v > 500):
            raise ValueError('Max participants debe estar entre 1 y 500')
        return v
    
    @validator('duration_minutes')
    def validate_duration(cls, v):
        if v is not None and (v < 1 or v > 1440):  # máximo 24 horas
            raise ValueError('Duration debe estar entre 1 y 1440 minutos')
        return v


class MeetingCreate(MeetingBase):
    """Esquema para crear reunión"""
    title: str
    project_id: int
    start_time: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Revisión de Progreso - Rediseño Web",
                "description": "Reunión semanal para revisar el progreso del proyecto",
                "project_id": 1,
                "start_time": "2024-02-15T10:00:00Z",
                "duration_minutes": 60,
                "is_recording_enabled": True,
                "max_participants": 10,
                "require_password": False,
                "waiting_room_enabled": True,
                "jitsi_config": {
                    "enableChat": True,
                    "enableScreenSharing": True,
                    "enableRecording": True
                }
            }
        }


class MeetingUpdate(MeetingBase):
    """Esquema para actualizar reunión"""
    title: Optional[str] = None
    project_id: Optional[int] = None
    start_time: Optional[datetime] = None
    status: Optional[str] = None
    recording_url: Optional[str] = None
    recording_status: Optional[str] = None
    participants_count: Optional[int] = None
    participants_data: Optional[List[Dict[str, Any]]] = None
    
    @validator('status')
    def validate_status(cls, v):
        if v is not None:
            allowed_statuses = ['scheduled', 'in-progress', 'completed', 'cancelled']
            if v not in allowed_statuses:
                raise ValueError(f'Status debe ser uno de: {", ".join(allowed_statuses)}')
        return v
    
    @validator('recording_status')
    def validate_recording_status(cls, v):
        if v is not None:
            allowed_statuses = ['none', 'recording', 'processing', 'ready', 'failed']
            if v not in allowed_statuses:
                raise ValueError(f'Recording status debe ser uno de: {", ".join(allowed_statuses)}')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "completed",
                "end_time": "2024-02-15T11:00:00Z",
                "participants_count": 5,
                "recording_status": "ready",
                "recording_url": "https://recordings.example.com/meeting-123.mp4",
                "meeting_notes": "Se revisó el progreso del diseño. Próximos pasos definidos."
            }
        }


class MeetingInDBBase(MeetingBase):
    """Esquema base para reunión en base de datos"""
    id: int
    room_id: str
    meeting_url: Optional[str] = None
    status: str
    recording_url: Optional[str] = None
    recording_status: str
    participants_count: int
    participants_data: Optional[List[Dict[str, Any]]] = None
    project_id: int
    created_by_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class Meeting(MeetingInDBBase):
    """Esquema para reunión (respuesta)"""
    project: Optional[ProjectSummary] = None
    created_by: Optional[UserProfile] = None
    is_active: Optional[bool] = None
    is_upcoming: Optional[bool] = None
    is_past: Optional[bool] = None
    jitsi_url: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Revisión de Progreso - Rediseño Web",
                "description": "Reunión semanal para revisar el progreso",
                "room_id": "v1tr0-meeting-abc123",
                "meeting_url": "https://meet.jit.si/v1tr0-meeting-abc123",
                "start_time": "2024-02-15T10:00:00Z",
                "end_time": "2024-02-15T11:00:00Z",
                "duration_minutes": 60,
                "status": "completed",
                "is_recording_enabled": True,
                "recording_url": "https://recordings.example.com/meeting-123.mp4",
                "recording_status": "ready",
                "max_participants": 10,
                "participants_count": 5,
                "require_password": False,
                "waiting_room_enabled": True,
                "project_id": 1,
                "created_by_id": 1,
                "is_active": False,
                "is_upcoming": False,
                "is_past": True,
                "jitsi_url": "https://meet.jit.si/v1tr0-meeting-abc123",
                "created_at": "2024-02-10T00:00:00Z",
                "updated_at": "2024-02-15T11:05:00Z"
            }
        }


class MeetingInDB(MeetingInDBBase):
    """Esquema para reunión en base de datos (con campos internos)"""
    pass


class MeetingSummary(BaseModel):
    """Esquema para resumen de reunión"""
    id: int
    title: str
    start_time: datetime
    status: str
    project_title: Optional[str] = None
    participants_count: int
    recording_status: str
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Revisión de Progreso",
                "start_time": "2024-02-15T10:00:00Z",
                "status": "completed",
                "project_title": "Rediseño Web Corporativo",
                "participants_count": 5,
                "recording_status": "ready"
            }
        }


class MeetingJoinRequest(BaseModel):
    """Esquema para solicitud de unirse a reunión"""
    participant_name: str
    participant_email: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "participant_name": "Juan Pérez",
                "participant_email": "juan@ejemplo.com"
            }
        }


class MeetingJoinResponse(BaseModel):
    """Esquema para respuesta de unirse a reunión"""
    meeting_url: str
    room_id: str
    participant_token: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "meeting_url": "https://meet.jit.si/v1tr0-meeting-abc123",
                "room_id": "v1tr0-meeting-abc123",
                "participant_token": "jwt-token-for-participant"
            }
        }