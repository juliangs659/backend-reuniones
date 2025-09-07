from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Client(BaseModel):
    """Modelo de cliente"""
    __tablename__ = "clients"
    
    # Campos básicos
    name = Column(String(255), nullable=False, index=True)
    company = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True, index=True)
    phone = Column(String(50), nullable=True)
    
    # Información de contacto
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=True)
    
    # Información adicional
    website = Column(String(500), nullable=True)
    industry = Column(String(100), nullable=True)
    company_size = Column(String(50), nullable=True)  # small, medium, large, enterprise
    
    # Campos de gestión
    status = Column(String(20), default="active", nullable=False)  # active, inactive, prospect
    notes = Column(Text, nullable=True)
    priority = Column(String(20), default="medium", nullable=False)  # low, medium, high
    
    # Información financiera
    tax_id = Column(String(50), nullable=True)
    billing_email = Column(String(255), nullable=True)
    payment_terms = Column(Integer, default=30, nullable=True)  # días
    
    # Relación con usuario (quien creó el cliente)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_by = relationship("User", foreign_keys=[created_by_id])
    
    # Relaciones
    projects = relationship("Project", back_populates="client", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Client(id={self.id}, name='{self.name}', company='{self.company}')>"
    
    @property
    def display_name(self):
        """Nombre para mostrar (prioriza company sobre name)"""
        return self.company if self.company else self.name