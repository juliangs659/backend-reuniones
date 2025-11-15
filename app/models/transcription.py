from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import Field, EmailStr
from app.models.base import MongoBaseModel, PyObjectId


class Transcription(MongoBaseModel):
    """
    Transcripción de reunión de Microsoft Teams.
    Se sube manualmente y se procesa con IA para extraer requerimientos.
    """
    # Datos básicos
    transcription_text: str = Field(..., description="Texto completo de la transcripción")
    user_email: str = Field(..., description="Email del usuario que sube la transcripción")
    meeting_id: Optional[PyObjectId] = Field(None, description="ID de la reunión asociada")
    project_id: Optional[PyObjectId] = Field(None, description="ID del proyecto asociado")
    
    # Metadata
    language: str = Field(default="es", description="Idioma de la transcripción")
    source: str = Field(default="teams", description="Origen: teams, manual, etc")
    
    # Estado de procesamiento
    status: str = Field(default="pending", description="pending, processing, completed, error")
    processed_at: Optional[datetime] = Field(None, description="Cuándo se procesó con IA")
    error_message: Optional[str] = None
    
    # Análisis de IA (resultado del procesamiento con OpenAI)
    ai_analysis: Optional[Dict[str, Any]] = Field(
        None, 
        description="Resultado del análisis de IA: requerimientos, fases, resumen"
    )
    ai_model_used: Optional[str] = Field(None, description="Modelo de IA usado (ej: gpt-4)")
    
    # Timestamps
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
