from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import BaseModel


class Meeting(BaseModel):
    """Modelo de reunión"""
    __tablename__ = "meetings"
    
    # Campos básicos
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Configuración de la reunión
    room_id = Column(String(255), unique=True, nullable=False, index=True)
    meeting_url = Column(String(500), nullable=True)
    password = Column(String(100), nullable=True)
    
    # Fechas y horarios
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    
    # Estado
    status = Column(String(20), default="scheduled", nullable=False)  # scheduled, in-progress, completed, cancelled
    
    # Configuración de grabación
    is_recording_enabled = Column(Boolean, default=True, nullable=False)
    recording_url = Column(String(500), nullable=True)
    recording_status = Column(String(20), default="none", nullable=False)  # none, recording, processing, ready, failed
    
    # Participantes y configuración
    max_participants = Column(Integer, default=50, nullable=False)
    require_password = Column(Boolean, default=False, nullable=False)
    waiting_room_enabled = Column(Boolean, default=False, nullable=False)
    
    # Metadatos
    participants_count = Column(Integer, default=0, nullable=False)
    participants_data = Column(JSON, nullable=True)  # Lista de participantes con metadata
    meeting_notes = Column(Text, nullable=True)
    
    # Configuración de Jitsi
    jitsi_config = Column(JSON, nullable=True)  # Configuración específica de Jitsi
    
    # Relaciones
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    project = relationship("Project", back_populates="meetings")
    
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_by = relationship("User", foreign_keys=[created_by_id])
    
    # Relación con transcripciones
    transcriptions = relationship("Transcription", back_populates="meeting", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Meeting(id={self.id}, title='{self.title}', status='{self.status}')>"
    
    @property
    def is_active(self):
        """Verificar si la reunión está activa"""
        return self.status == "in-progress"
    
    @property
    def is_upcoming(self):
        """Verificar si la reunión es próxima"""
        if self.status == "scheduled":
            return self.start_time > datetime.utcnow()
        return False
    
    @property
    def is_past(self):
        """Verificar si la reunión ya pasó"""
        if self.end_time:
            return self.end_time < datetime.utcnow()
        elif self.start_time:
            # Si no hay end_time, asumir que duró 1 hora
            estimated_end = self.start_time
            if self.duration_minutes:
                from datetime import timedelta
                estimated_end = self.start_time + timedelta(minutes=self.duration_minutes)
            else:
                from datetime import timedelta
                estimated_end = self.start_time + timedelta(hours=1)
            return estimated_end < datetime.utcnow()
        return False
    
    def generate_jitsi_url(self, domain: str = "meet.jit.si"):
        """Generar URL de Jitsi Meet"""
        return f"https://{domain}/{self.room_id}"