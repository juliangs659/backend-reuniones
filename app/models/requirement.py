from datetime import datetime
from typing import Optional
from pydantic import Field
from app.models.base import MongoBaseModel, PyObjectId


class Requirement(MongoBaseModel):
    """
    Requerimiento extraído de una transcripción mediante IA.
    Cada requerimiento pertenece a una fase del proyecto.
    """
    # Relaciones
    project_id: PyObjectId = Field(..., description="ID del proyecto")
    phase_id: PyObjectId = Field(..., description="ID de la fase a la que pertenece")
    transcription_id: Optional[PyObjectId] = Field(
        None, 
        description="ID de la transcripción de donde se extrajo"
    )
    
    # Datos del requerimiento
    title: str = Field(..., description="Título del requerimiento")
    description: str = Field(..., description="Descripción detallada")
    
    # Clasificación
    type: str = Field(
        default="functional",
        description="functional, non_functional, technical, business"
    )
    priority: str = Field(
        default="medium",
        description="low, medium, high, critical"
    )
    
    # Estado
    status: str = Field(
        default="pending",
        description="pending, in_progress, completed, rejected"
    )
    
    # Metadata
    extracted_by_ai: bool = Field(default=True, description="Si fue extraído por IA")
    user_edited: bool = Field(default=False, description="Si fue editado por el usuario")
    
    # Timestamps
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
