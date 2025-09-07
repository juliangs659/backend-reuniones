from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey, DateTime, JSON, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import BaseModel


class ChatMessage(BaseModel):
    """Modelo de mensaje de chat con IA"""
    __tablename__ = "chat_messages"
    
    # Contenido del mensaje
    message = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=True)
    
    # Tipo de mensaje
    message_type = Column(String(20), default="chat", nullable=False)  # chat, question, command, system
    
    # Contexto utilizado por la IA
    context_used = Column(JSON, nullable=True)  # Documentos/datos utilizados para la respuesta
    context_sources = Column(JSON, nullable=True)  # Fuentes específicas (transcripciones, documentos, etc.)
    
    # Metadatos de la IA
    ai_model_used = Column(String(100), nullable=True)  # gpt-4, gpt-3.5-turbo, etc.
    tokens_used = Column(Integer, nullable=True)
    response_time_ms = Column(Integer, nullable=True)
    confidence_score = Column(Float, nullable=True)  # 0.0 - 1.0
    
    # Estado del procesamiento
    processing_status = Column(String(20), default="completed", nullable=False)  # pending, processing, completed, failed
    error_message = Column(Text, nullable=True)
    
    # Configuración del mensaje
    is_pinned = Column(Boolean, default=False, nullable=False)
    is_important = Column(Boolean, default=False, nullable=False)
    is_private = Column(Boolean, default=False, nullable=False)
    
    # Feedback del usuario
    user_rating = Column(Integer, nullable=True)  # 1-5 estrellas
    user_feedback = Column(Text, nullable=True)
    
    # Metadatos adicionales
    tags = Column(JSON, nullable=True)  # Tags para categorizar mensajes
    custom_data = Column(JSON, nullable=True)  # Datos personalizados
    
    # Fechas específicas
    ai_responded_at = Column(DateTime, nullable=True)
    
    # Relaciones
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    project = relationship("Project", back_populates="chat_messages")
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="chat_messages")
    
    # Relación con mensaje padre (para hilos de conversación)
    parent_message_id = Column(Integer, ForeignKey("chat_messages.id"), nullable=True)
    parent_message = relationship("ChatMessage", remote_side="ChatMessage.id", backref="replies")
    
    def __repr__(self):
        return f"<ChatMessage(id={self.id}, project_id={self.project_id}, type='{self.message_type}')>"
    
    @property
    def has_ai_response(self):
        """Verificar si tiene respuesta de IA"""
        return self.ai_response is not None and len(self.ai_response.strip()) > 0
    
    @property
    def is_completed(self):
        """Verificar si el procesamiento está completado"""
        return self.processing_status == "completed"
    
    @property
    def is_failed(self):
        """Verificar si el procesamiento falló"""
        return self.processing_status == "failed"
    
    @property
    def response_time_seconds(self):
        """Tiempo de respuesta en segundos"""
        if self.response_time_ms:
            return self.response_time_ms / 1000.0
        return None
    
    @property
    def word_count(self):
        """Contar palabras en el mensaje"""
        if self.message:
            return len(self.message.split())
        return 0
    
    @property
    def ai_response_word_count(self):
        """Contar palabras en la respuesta de IA"""
        if self.ai_response:
            return len(self.ai_response.split())
        return 0
    
    def get_context_summary(self):
        """Obtener resumen del contexto utilizado"""
        if self.context_used:
            sources = []
            for context in self.context_used:
                if isinstance(context, dict) and 'source' in context:
                    sources.append(context['source'])
            return sources
        return []