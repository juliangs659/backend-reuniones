from sqlalchemy import Column, String, Boolean, Text
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class User(BaseModel):
    """Modelo de usuario"""
    __tablename__ = "users"
    
    # Campos básicos
    supabase_id = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    
    # Campos de estado
    is_active = Column(Boolean, default=True, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    
    # Campos adicionales
    phone = Column(String(50), nullable=True)
    company = Column(String(255), nullable=True)
    position = Column(String(255), nullable=True)
    bio = Column(Text, nullable=True)
    
    # Configuración de usuario
    timezone = Column(String(50), default="UTC", nullable=False)
    language = Column(String(10), default="es", nullable=False)
    
    # Relaciones
    projects = relationship("Project", back_populates="owner", cascade="all, delete-orphan")
    chat_messages = relationship("ChatMessage", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', full_name='{self.full_name}')>"