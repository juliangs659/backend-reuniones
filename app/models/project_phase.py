from datetime import datetime
from typing import Optional, List
from pydantic import Field
from app.models.base import MongoBaseModel, PyObjectId


class ProjectPhase(MongoBaseModel):
    """
    Fase o etapa del proyecto.
    Cada proyecto se divide en fases generales (ej: Análisis, Diseño, Desarrollo, Testing, Despliegue)
    """
    # Relación con proyecto
    project_id: PyObjectId = Field(..., description="ID del proyecto al que pertenece")
    
    # Datos de la fase
    name: str = Field(..., description="Nombre de la fase (ej: Análisis de Requerimientos)")
    description: Optional[str] = Field(None, description="Descripción detallada de la fase")
    
    # Estado y orden
    status: str = Field(
        default="pending", 
        description="pending, in_progress, completed, blocked"
    )
    order: int = Field(..., description="Orden de la fase en el proyecto (1, 2, 3...)")
    
    # Fechas
    start_date: Optional[datetime] = Field(None, description="Fecha de inicio planificada")
    end_date: Optional[datetime] = Field(None, description="Fecha de fin planificada")
    actual_start_date: Optional[datetime] = Field(None, description="Fecha real de inicio")
    actual_end_date: Optional[datetime] = Field(None, description="Fecha real de finalización")
    
    # Progreso
    completion_percentage: int = Field(default=0, ge=0, le=100)
    
    # Timestamps
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
