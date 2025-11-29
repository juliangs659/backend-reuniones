from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import Field
from app.models.base import MongoBaseModel, PyObjectId


class Project(MongoBaseModel):
    title: str = Field(..., index=True)
    description: Optional[str] = None
    
    status: str = "planned"
    progress: int = 0
    priority: str = "medium"
    
    # Fase actual del proyecto
    current_phase_id: Optional[PyObjectId] = Field(
        None, 
        description="ID de la fase actual en la que se encuentra el proyecto"
    )
    completion_percentage: int = Field(
        default=0, 
        ge=0, 
        le=100,
        description="Porcentaje de completitud general del proyecto"
    )
    
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    deadline: Optional[datetime] = None
    
    budget: Optional[float] = None
    hourly_rate: Optional[float] = None
    estimated_hours: Optional[int] = None
    actual_hours: int = 0
    
    is_billable: bool = True
    is_active: bool = True
    
    tags: Optional[List[str]] = None
    custom_fields: Optional[Dict[str, Any]] = None
    
    client_id: PyObjectId
    owner_id: PyObjectId
    
    # Timestamps
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
