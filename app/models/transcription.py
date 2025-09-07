from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey, DateTime, Float, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import BaseModel


class Transcription(BaseModel):
    """Modelo de transcripción de audio"""
    __tablename__ = "transcriptions"
    
    # Campos básicos
    title = Column(String(255), nullable=True)
    
    # Contenido de la transcripción
    transcript_text = Column(Text, nullable=True)
    original_language = Column(String(10), default="es", nullable=False)
    
    # Procesamiento con IA
    summary = Column(Text, nullable=True)
    key_points = Column(JSON, nullable=True)  # Lista de puntos clave
    commitments = Column(JSON, nullable=True)  # Lista de compromisos
    next_steps = Column(JSON, nullable=True)  # Lista de próximos pasos
    participants = Column(JSON, nullable=True)  # Lista de participantes identificados
    
    # Metadatos del audio
    audio_filename = Column(String(500), nullable=True)
    audio_duration_seconds = Column(Integer, nullable=True)
    audio_format = Column(String(20), nullable=True)
    audio_size_bytes = Column(Integer, nullable=True)
    
    # Estado del procesamiento
    processing_status = Column(String(20), default="pending", nullable=False)  # pending, processing, completed, failed
    confidence_score = Column(Float, nullable=True)  # 0.0 - 1.0
    
    # Fechas de procesamiento
    processing_started_at = Column(DateTime, nullable=True)
    processing_completed_at = Column(DateTime, nullable=True)
    
    # Configuración del procesamiento
    ai_model_used = Column(String(100), nullable=True)  # whisper-1, etc.
    processing_options = Column(JSON, nullable=True)  # Opciones específicas del procesamiento
    
    # Errores y logs
    error_message = Column(Text, nullable=True)
    processing_logs = Column(JSON, nullable=True)
    
    # Configuración de privacidad
    is_sensitive = Column(Boolean, default=False, nullable=False)
    retention_days = Column(Integer, default=365, nullable=False)
    
    # Relaciones
    meeting_id = Column(Integer, ForeignKey("meetings.id"), nullable=False)
    meeting = relationship("Meeting", back_populates="transcriptions")
    
    processed_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    processed_by = relationship("User", foreign_keys=[processed_by_id])
    
    def __repr__(self):
        return f"<Transcription(id={self.id}, meeting_id={self.meeting_id}, status='{self.processing_status}')>"
    
    @property
    def is_completed(self):
        """Verificar si el procesamiento está completado"""
        return self.processing_status == "completed"
    
    @property
    def is_failed(self):
        """Verificar si el procesamiento falló"""
        return self.processing_status == "failed"
    
    @property
    def processing_duration_seconds(self):
        """Duración del procesamiento en segundos"""
        if self.processing_started_at and self.processing_completed_at:
            delta = self.processing_completed_at - self.processing_started_at
            return delta.total_seconds()
        return None
    
    @property
    def word_count(self):
        """Contar palabras en la transcripción"""
        if self.transcript_text:
            return len(self.transcript_text.split())
        return 0
    
    @property
    def should_be_deleted(self):
        """Verificar si la transcripción debe ser eliminada por retención"""
        if self.retention_days and self.created_at:
            from datetime import timedelta
            expiry_date = self.created_at + timedelta(days=self.retention_days)
            return datetime.utcnow() > expiry_date
        return False