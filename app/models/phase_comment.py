from datetime import datetime
from typing import Optional
from pydantic import Field
from app.models.base import MongoBaseModel, PyObjectId


class PhaseComment(MongoBaseModel):
    """
    Comentario del usuario sobre una fase del proyecto.
    Permite feedback y comunicación sobre el progreso de cada fase.
    """
    # Relaciones
    phase_id: PyObjectId = Field(..., description="ID de la fase comentada")
    project_id: PyObjectId = Field(..., description="ID del proyecto")
    
    # Datos del comentario
    user_email: str = Field(..., description="Email del usuario que comenta")
    comment: str = Field(..., description="Texto del comentario")
    
    # Metadata
    is_internal: bool = Field(
        default=False, 
        description="Si es interno (no visible para cliente)"
    )
    
    # Timestamps
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
