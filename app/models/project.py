from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey, DateTime, Numeric, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import BaseModel


class Project(BaseModel):
    """Modelo de proyecto"""
    __tablename__ = "projects"
    
    # Campos básicos
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Estado y progreso
    status = Column(String(20), default="planned", nullable=False)  # planned, in-progress, completed, on-hold, cancelled
    progress = Column(Integer, default=0, nullable=False)  # 0-100
    priority = Column(String(20), default="medium", nullable=False)  # low, medium, high, urgent
    
    # Fechas
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    deadline = Column(DateTime, nullable=True)
    
    # Información financiera
    budget = Column(Numeric(10, 2), nullable=True)
    hourly_rate = Column(Numeric(8, 2), nullable=True)
    estimated_hours = Column(Integer, nullable=True)
    actual_hours = Column(Integer, default=0, nullable=False)
    
    # Configuración
    is_billable = Column(Boolean, default=True, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Metadatos adicionales
    tags = Column(JSON, nullable=True)  # Lista de tags
    custom_fields = Column(JSON, nullable=True)  # Campos personalizados
    
    # Relaciones
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    client = relationship("Client", back_populates="projects")
    
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="projects")
    
    # Relaciones con otros modelos
    meetings = relationship("Meeting", back_populates="project", cascade="all, delete-orphan")
    chat_messages = relationship("ChatMessage", back_populates="project", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Project(id={self.id}, title='{self.title}', status='{self.status}')>"
    
    @property
    def is_overdue(self):
        """Verificar si el proyecto está atrasado"""
        if self.deadline and self.status not in ['completed', 'cancelled']:
            return datetime.utcnow() > self.deadline
        return False
    
    @property
    def days_remaining(self):
        """Días restantes hasta la fecha límite"""
        if self.deadline and self.status not in ['completed', 'cancelled']:
            delta = self.deadline - datetime.utcnow()
            return delta.days
        return None
    
    @property
    def budget_utilization(self):
        """Porcentaje de presupuesto utilizado"""
        if self.budget and self.hourly_rate and self.actual_hours:
            spent = float(self.hourly_rate) * self.actual_hours
            return (spent / float(self.budget)) * 100
        return 0