from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, validator


class ClientBase(BaseModel):
    """Esquema base para cliente"""
    name: str
    company: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    company_size: Optional[str] = None
    status: Optional[str] = "active"
    notes: Optional[str] = None
    priority: Optional[str] = "medium"
    tax_id: Optional[str] = None
    billing_email: Optional[EmailStr] = None
    payment_terms: Optional[int] = 30
    
    @validator('status')
    def validate_status(cls, v):
        allowed_statuses = ['active', 'inactive', 'prospect']
        if v not in allowed_statuses:
            raise ValueError(f'Status debe ser uno de: {", ".join(allowed_statuses)}')
        return v
    
    @validator('priority')
    def validate_priority(cls, v):
        allowed_priorities = ['low', 'medium', 'high']
        if v not in allowed_priorities:
            raise ValueError(f'Priority debe ser uno de: {", ".join(allowed_priorities)}')
        return v
    
    @validator('company_size')
    def validate_company_size(cls, v):
        if v is not None:
            allowed_sizes = ['small', 'medium', 'large', 'enterprise']
            if v not in allowed_sizes:
                raise ValueError(f'Company size debe ser uno de: {", ".join(allowed_sizes)}')
        return v


class ClientCreate(ClientBase):
    """Esquema para crear cliente"""
    name: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Juan Pérez",
                "company": "TechCorp S.A.",
                "email": "juan@techcorp.com",
                "phone": "+34 600 123 456",
                "address": "Calle Mayor 123",
                "city": "Madrid",
                "country": "España",
                "postal_code": "28001",
                "website": "https://techcorp.com",
                "industry": "Tecnología",
                "company_size": "medium",
                "status": "active",
                "priority": "high",
                "notes": "Cliente importante con múltiples proyectos",
                "tax_id": "B12345678",
                "billing_email": "facturacion@techcorp.com",
                "payment_terms": 30
            }
        }


class ClientUpdate(ClientBase):
    """Esquema para actualizar cliente"""
    name: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Juan Pérez García",
                "phone": "+34 600 987 654",
                "status": "active",
                "priority": "high",
                "notes": "Cliente VIP - respuesta prioritaria"
            }
        }


class ClientInDBBase(ClientBase):
    """Esquema base para cliente en base de datos"""
    id: int
    created_by_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class Client(ClientInDBBase):
    """Esquema para cliente (respuesta)"""
    display_name: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Juan Pérez",
                "company": "TechCorp S.A.",
                "email": "juan@techcorp.com",
                "phone": "+34 600 123 456",
                "address": "Calle Mayor 123",
                "city": "Madrid",
                "country": "España",
                "postal_code": "28001",
                "website": "https://techcorp.com",
                "industry": "Tecnología",
                "company_size": "medium",
                "status": "active",
                "priority": "high",
                "notes": "Cliente importante",
                "tax_id": "B12345678",
                "billing_email": "facturacion@techcorp.com",
                "payment_terms": 30,
                "display_name": "TechCorp S.A.",
                "created_by_id": 1,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
        }


class ClientInDB(ClientInDBBase):
    """Esquema para cliente en base de datos (con campos internos)"""
    pass


class ClientSummary(BaseModel):
    """Esquema para resumen de cliente"""
    id: int
    name: str
    company: Optional[str] = None
    email: Optional[str] = None
    status: str
    priority: str
    display_name: Optional[str] = None
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Juan Pérez",
                "company": "TechCorp S.A.",
                "email": "juan@techcorp.com",
                "status": "active",
                "priority": "high",
                "display_name": "TechCorp S.A."
            }
        }


class ClientStats(BaseModel):
    """Esquema para estadísticas de cliente"""
    total_projects: int
    active_projects: int
    completed_projects: int
    total_meetings: int
    total_revenue: Optional[float] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_projects": 8,
                "active_projects": 3,
                "completed_projects": 5,
                "total_meetings": 25,
                "total_revenue": 45000.00
            }
        }