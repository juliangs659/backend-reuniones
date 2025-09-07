from typing import Optional, List, Any
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, validator
from app.schemas.client import ClientSummary
from app.schemas.user import UserProfile


class ProjectBase(BaseModel):
    """Esquema base para proyecto"""
    title: str
    description: Optional[str] = None
    status: Optional[str] = "planned"
    progress: Optional[int] = 0
    priority: Optional[str] = "medium"
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    deadline: Optional[datetime] = None
    budget: Optional[Decimal] = None
    hourly_rate: Optional[Decimal] = None
    estimated_hours: Optional[int] = None
    is_billable: Optional[bool] = True
    is_active: Optional[bool] = True
    tags: Optional[List[str]] = None
    custom_fields: Optional[dict] = None
    
    @validator('status')
    def validate_status(cls, v):
        allowed_statuses = ['planned', 'in-progress', 'completed', 'on-hold', 'cancelled']
        if v not in allowed_statuses:
            raise ValueError(f'Status debe ser uno de: {", ".join(allowed_statuses)}')
        return v
    
    @validator('priority')
    def validate_priority(cls, v):
        allowed_priorities = ['low', 'medium', 'high', 'urgent']
        if v not in allowed_priorities:
            raise ValueError(f'Priority debe ser uno de: {", ".join(allowed_priorities)}')
        return v
    
    @validator('progress')
    def validate_progress(cls, v):
        if v is not None and (v < 0 or v > 100):
            raise ValueError('Progress debe estar entre 0 y 100')
        return v


class ProjectCreate(ProjectBase):
    """Esquema para crear proyecto"""
    title: str
    client_id: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Rediseño Web Corporativo",
                "description": "Rediseño completo del sitio web corporativo con nueva identidad visual",
                "client_id": 1,
                "status": "planned",
                "priority": "high",
                "start_date": "2024-02-01T00:00:00Z",
                "deadline": "2024-07-15T23:59:59Z",
                "budget": 25000.00,
                "hourly_rate": 75.00,
                "estimated_hours": 300,
                "is_billable": True,
                "tags": ["web", "diseño", "frontend"],
                "custom_fields": {
                    "technology_stack": "React, TypeScript, Tailwind",
                    "design_system": "Material Design"
                }
            }
        }


class ProjectUpdate(ProjectBase):
    """Esquema para actualizar proyecto"""
    title: Optional[str] = None
    client_id: Optional[int] = None
    actual_hours: Optional[int] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "in-progress",
                "progress": 45,
                "actual_hours": 135,
                "notes": "Progreso según lo planificado"
            }
        }


class ProjectInDBBase(ProjectBase):
    """Esquema base para proyecto en base de datos"""
    id: int
    client_id: int
    owner_id: int
    actual_hours: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class Project(ProjectInDBBase):
    """Esquema para proyecto (respuesta)"""
    client: Optional[ClientSummary] = None
    owner: Optional[UserProfile] = None
    is_overdue: Optional[bool] = None
    days_remaining: Optional[int] = None
    budget_utilization: Optional[float] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Rediseño Web Corporativo",
                "description": "Rediseño completo del sitio web corporativo",
                "status": "in-progress",
                "progress": 75,
                "priority": "high",
                "start_date": "2024-02-01T00:00:00Z",
                "end_date": None,
                "deadline": "2024-07-15T23:59:59Z",
                "budget": 25000.00,
                "hourly_rate": 75.00,
                "estimated_hours": 300,
                "actual_hours": 225,
                "is_billable": True,
                "is_active": True,
                "tags": ["web", "diseño", "frontend"],
                "client_id": 1,
                "owner_id": 1,
                "is_overdue": False,
                "days_remaining": 45,
                "budget_utilization": 67.5,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-15T00:00:00Z"
            }
        }


class ProjectInDB(ProjectInDBBase):
    """Esquema para proyecto en base de datos (con campos internos)"""
    pass


class ProjectSummary(BaseModel):
    """Esquema para resumen de proyecto"""
    id: int
    title: str
    status: str
    progress: int
    priority: str
    client_name: Optional[str] = None
    deadline: Optional[datetime] = None
    is_overdue: Optional[bool] = None
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Rediseño Web Corporativo",
                "status": "in-progress",
                "progress": 75,
                "priority": "high",
                "client_name": "TechCorp S.A.",
                "deadline": "2024-07-15T23:59:59Z",
                "is_overdue": False
            }
        }


class ProjectStats(BaseModel):
    """Esquema para estadísticas de proyecto"""
    total_meetings: int
    total_transcriptions: int
    total_chat_messages: int
    hours_logged: int
    budget_spent: Optional[float] = None
    completion_percentage: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_meetings": 12,
                "total_transcriptions": 8,
                "total_chat_messages": 45,
                "hours_logged": 225,
                "budget_spent": 16875.00,
                "completion_percentage": 75
            }
        }


class ProjectFilter(BaseModel):
    """Esquema para filtros de proyecto"""
    status: Optional[str] = None
    priority: Optional[str] = None
    client_id: Optional[int] = None
    owner_id: Optional[int] = None
    is_active: Optional[bool] = None
    is_overdue: Optional[bool] = None
    tags: Optional[List[str]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "in-progress",
                "priority": "high",
                "client_id": 1,
                "is_active": True,
                "tags": ["web", "frontend"]
            }
        }