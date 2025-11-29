from datetime import datetime
from typing import Optional, List
from pydantic import Field
from app.models.base import MongoBaseModel, PyObjectId


class Meeting(MongoBaseModel):
    title: str = Field(..., index=True)
    description: Optional[str] = None
    
    scheduled_at: datetime
    duration_minutes: int = 60
    actual_duration_minutes: Optional[int] = None
    
    status: str = "scheduled"
    
    jitsi_room_name: Optional[str] = None
    jitsi_url: Optional[str] = None
    
    participant_ids: List[PyObjectId] = []
    host_id: PyObjectId
    
    project_id: PyObjectId
    
    notes: Optional[str] = None
    action_items: Optional[List[str]] = None
