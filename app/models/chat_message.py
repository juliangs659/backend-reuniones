from typing import Optional
from pydantic import Field
from app.models.base import MongoBaseModel, PyObjectId


class ChatMessage(MongoBaseModel):
    message: str = Field(..., min_length=1)
    response: Optional[str] = None
    
    message_type: str = "user"
    context_type: Optional[str] = None
    
    status: str = "pending"
    error_message: Optional[str] = None
    
    model_used: Optional[str] = None
    tokens_used: Optional[int] = None
    processing_time_ms: Optional[int] = None
    
    user_id: PyObjectId
    project_id: Optional[PyObjectId] = None
    meeting_id: Optional[PyObjectId] = None
    transcription_id: Optional[PyObjectId] = None
    
    conversation_id: Optional[str] = None
    parent_message_id: Optional[PyObjectId] = None
