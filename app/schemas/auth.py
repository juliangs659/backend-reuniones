from typing import Optional
from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    """Esquema para token de acceso"""
    access_token: str
    token_type: str = "bearer"
    expires_in: Optional[int] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 3600
            }
        }


class TokenData(BaseModel):
    """Datos del token decodificado"""
    user_id: Optional[str] = None
    email: Optional[str] = None
    

class LoginRequest(BaseModel):
    """Esquema para solicitud de login"""
    email: EmailStr
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "usuario@ejemplo.com",
                "password": "mi_contraseña_segura"
            }
        }


class RegisterRequest(BaseModel):
    """Esquema para solicitud de registro"""
    email: EmailStr
    password: str
    full_name: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "nuevo@ejemplo.com",
                "password": "contraseña_segura123",
                "full_name": "Juan Pérez"
            }
        }


class PasswordResetRequest(BaseModel):
    """Esquema para solicitud de restablecimiento de contraseña"""
    email: EmailStr
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "usuario@ejemplo.com"
            }
        }


class PasswordResetConfirm(BaseModel):
    """Esquema para confirmación de restablecimiento de contraseña"""
    token: str
    new_password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "token": "reset_token_here",
                "new_password": "nueva_contraseña_segura"
            }
        }


class RefreshTokenRequest(BaseModel):
    """Esquema para solicitud de refresh token"""
    refresh_token: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "refresh_token": "refresh_token_here"
            }
        }