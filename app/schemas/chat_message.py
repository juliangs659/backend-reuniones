from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, validator
from app.schemas.project import ProjectSummary
from app.schemas.user import UserProfile


class ChatMessageBase(BaseModel):
    """Esquema base para mensaje de chat"""
    message: str
    message_type: Optional[str] = "chat"
    is_pinned: Optional[bool] = False
    is_important: Optional[bool] = False
    is_private: Optional[bool] = False
    tags: Optional[List[str]] = None
    custom_data: Optional[Dict[str, Any]] = None
    
    @validator('message_type')
    def validate_message_type(cls, v):
        allowed_types = ['chat', 'question', 'command', 'system']
        if v not in allowed_types:
            raise ValueError(f'Message type debe ser uno de: {", ".join(allowed_types)}')
        return v


class ChatMessageCreate(ChatMessageBase):
    """Esquema para crear mensaje de chat"""
    message: str
    project_id: int
    parent_message_id: Optional[int] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "¿Cuál es el progreso actual del proyecto de rediseño web?",
                "project_id": 1,
                "message_type": "question",
                "is_important": True,
                "tags": ["progreso", "estado"]
            }
        }


class ChatMessageUpdate(ChatMessageBase):
    """Esquema para actualizar mensaje de chat"""
    message: Optional[str] = None
    ai_response: Optional[str] = None
    context_used: Optional[List[Dict[str, Any]]] = None
    context_sources: Optional[List[Dict[str, Any]]] = None
    processing_status: Optional[str] = None
    ai_model_used: Optional[str] = None
    tokens_used: Optional[int] = None
    response_time_ms: Optional[int] = None
    confidence_score: Optional[float] = None
    error_message: Optional[str] = None
    user_rating: Optional[int] = None
    user_feedback: Optional[str] = None
    ai_responded_at: Optional[datetime] = None
    
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
    
    @validator('user_rating')
    def validate_user_rating(cls, v):
        if v is not None and (v < 1 or v > 5):
            raise ValueError('User rating debe estar entre 1 y 5')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "ai_response": "Según la información más reciente, el proyecto está al 75% de completado...",
                "processing_status": "completed",
                "ai_model_used": "gpt-4",
                "tokens_used": 150,
                "response_time_ms": 2500,
                "confidence_score": 0.92,
                "user_rating": 5,
                "user_feedback": "Respuesta muy útil y precisa"
            }
        }


class ChatMessageInDBBase(ChatMessageBase):
    """Esquema base para mensaje de chat en base de datos"""
    id: int
    ai_response: Optional[str] = None
    context_used: Optional[List[Dict[str, Any]]] = None
    context_sources: Optional[List[Dict[str, Any]]] = None
    ai_model_used: Optional[str] = None
    tokens_used: Optional[int] = None
    response_time_ms: Optional[int] = None
    confidence_score: Optional[float] = None
    processing_status: str
    error_message: Optional[str] = None
    user_rating: Optional[int] = None
    user_feedback: Optional[str] = None
    ai_responded_at: Optional[datetime] = None
    project_id: int
    user_id: int
    parent_message_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ChatMessage(ChatMessageInDBBase):
    """Esquema para mensaje de chat (respuesta)"""
    project: Optional[ProjectSummary] = None
    user: Optional[UserProfile] = None
    parent_message: Optional['ChatMessage'] = None
    replies: Optional[List['ChatMessage']] = None
    has_ai_response: Optional[bool] = None
    is_completed: Optional[bool] = None
    is_failed: Optional[bool] = None
    response_time_seconds: Optional[float] = None
    word_count: Optional[int] = None
    ai_response_word_count: Optional[int] = None
    context_summary: Optional[List[str]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "message": "¿Cuál es el progreso actual del proyecto?",
                "ai_response": "Según la información más reciente, el proyecto está al 75% completado. Se han completado las fases de diseño y desarrollo frontend...",
                "message_type": "question",
                "context_used": [
                    {
                        "source": "project_data",
                        "type": "project_status",
                        "data": {"progress": 75, "status": "in-progress"}
                    }
                ],
                "context_sources": [
                    {
                        "type": "transcription",
                        "id": 1,
                        "title": "Última reunión de progreso"
                    }
                ],
                "ai_model_used": "gpt-4",
                "tokens_used": 150,
                "response_time_ms": 2500,
                "confidence_score": 0.92,
                "processing_status": "completed",
                "is_pinned": False,
                "is_important": True,
                "is_private": False,
                "user_rating": 5,
                "user_feedback": "Respuesta muy útil",
                "tags": ["progreso", "estado"],
                "project_id": 1,
                "user_id": 1,
                "parent_message_id": None,
                "ai_responded_at": "2024-02-15T14:30:25Z",
                "has_ai_response": True,
                "is_completed": True,
                "is_failed": False,
                "response_time_seconds": 2.5,
                "word_count": 12,
                "ai_response_word_count": 45,
                "context_summary": ["project_data", "transcription"],
                "created_at": "2024-02-15T14:30:20Z",
                "updated_at": "2024-02-15T14:30:25Z"
            }
        }


class ChatMessageInDB(ChatMessageInDBBase):
    """Esquema para mensaje de chat en base de datos (con campos internos)"""
    pass


class ChatMessageSummary(BaseModel):
    """Esquema para resumen de mensaje de chat"""
    id: int
    message: str
    message_type: str
    has_ai_response: bool
    is_important: bool
    user_name: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "message": "¿Cuál es el progreso actual del proyecto?",
                "message_type": "question",
                "has_ai_response": True,
                "is_important": True,
                "user_name": "Juan Pérez",
                "created_at": "2024-02-15T14:30:20Z"
            }
        }


class ChatRequest(BaseModel):
    """Esquema para solicitud de chat"""
    message: str
    include_context: Optional[bool] = True
    context_limit: Optional[int] = 5
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "¿Cuáles fueron los puntos clave de la última reunión?",
                "include_context": True,
                "context_limit": 3
            }
        }


class ChatResponse(BaseModel):
    """Esquema para respuesta de chat"""
    message_id: int
    ai_response: str
    context_used: List[Dict[str, Any]]
    confidence_score: Optional[float] = None
    response_time_ms: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "message_id": 1,
                "ai_response": "Los puntos clave de la última reunión fueron...",
                "context_used": [
                    {
                        "source": "transcription",
                        "id": 1,
                        "title": "Reunión de progreso"
                    }
                ],
                "confidence_score": 0.95,
                "response_time_ms": 2500
            }
        }


class QuestionRequest(BaseModel):
    """Esquema para solicitud de pregunta específica"""
    question: str
    search_transcriptions: Optional[bool] = True
    search_meetings: Optional[bool] = True
    search_chat_history: Optional[bool] = True
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "¿Qué compromisos se establecieron en las últimas reuniones?",
                "search_transcriptions": True,
                "search_meetings": True,
                "search_chat_history": False
            }
        }


class InsightsResponse(BaseModel):
    """Esquema para respuesta de insights del proyecto"""
    project_summary: str
    key_insights: List[str]
    recent_activity: List[str]
    recommendations: List[str]
    risk_factors: List[str]
    
    class Config:
        json_schema_extra = {
            "example": {
                "project_summary": "El proyecto de rediseño web está progresando bien con un 75% de completado...",
                "key_insights": [
                    "El equipo está cumpliendo con los plazos establecidos",
                    "Se necesita más feedback del cliente"
                ],
                "recent_activity": [
                    "Última reunión: Revisión de mockups",
                    "Entrega de fase de diseño completada"
                ],
                "recommendations": [
                    "Programar sesión de feedback con el cliente",
                    "Revisar cronograma de desarrollo"
                ],
                "risk_factors": [
                    "Posible retraso si no se recibe feedback pronto"
                ]
            }
        }


# Actualizar referencias circulares
ChatMessage.model_rebuild()