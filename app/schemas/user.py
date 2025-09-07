from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, validator


class UserBase(BaseModel):
    """Esquema base para usuario"""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    position: Optional[str] = None
    bio: Optional[str] = None
    timezone: Optional[str] = "UTC"
    language: Optional[str] = "es"
    is_active: Optional[bool] = True
    is_admin: Optional[bool] = False


class UserCreate(UserBase):
    """Esquema para crear usuario"""
    email: EmailStr
    supabase_id: str
    full_name: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "usuario@ejemplo.com",
                "supabase_id": "uuid-from-supabase",
                "full_name": "Juan Pérez",
                "phone": "+34 600 123 456",
                "company": "Mi Empresa S.L.",
                "position": "Desarrollador",
                "timezone": "Europe/Madrid",
                "language": "es"
            }
        }


class UserUpdate(UserBase):
    """Esquema para actualizar usuario"""
    pass
    
    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "Juan Pérez García",
                "phone": "+34 600 123 456",
                "company": "Nueva Empresa S.L.",
                "position": "Senior Developer",
                "bio": "Desarrollador con 5 años de experiencia",
                "timezone": "Europe/Madrid"
            }
        }


class UserInDBBase(UserBase):
    """Esquema base para usuario en base de datos"""
    id: int
    supabase_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class User(UserInDBBase):
    """Esquema para usuario (respuesta)"""
    pass
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "supabase_id": "uuid-from-supabase",
                "email": "usuario@ejemplo.com",
                "full_name": "Juan Pérez",
                "avatar_url": "https://ejemplo.com/avatar.jpg",
                "phone": "+34 600 123 456",
                "company": "Mi Empresa S.L.",
                "position": "Desarrollador",
                "bio": "Desarrollador con experiencia en Python y React",
                "timezone": "Europe/Madrid",
                "language": "es",
                "is_active": True,
                "is_admin": False,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
        }


class UserInDB(UserInDBBase):
    """Esquema para usuario en base de datos (con campos internos)"""
    pass


class UserProfile(BaseModel):
    """Esquema para perfil público de usuario"""
    id: int
    full_name: str
    avatar_url: Optional[str] = None
    company: Optional[str] = None
    position: Optional[str] = None
    bio: Optional[str] = None
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "full_name": "Juan Pérez",
                "avatar_url": "https://ejemplo.com/avatar.jpg",
                "company": "Mi Empresa S.L.",
                "position": "Desarrollador",
                "bio": "Desarrollador con experiencia en Python y React"
            }
        }


class UserStats(BaseModel):
    """Esquema para estadísticas de usuario"""
    total_projects: int
    active_projects: int
    completed_projects: int
    total_meetings: int
    total_chat_messages: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_projects": 15,
                "active_projects": 5,
                "completed_projects": 10,
                "total_meetings": 45,
                "total_chat_messages": 120
            }
        }