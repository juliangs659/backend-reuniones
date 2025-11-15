from typing import Optional, List, Any
from datetime import datetime
from pydantic import BaseModel, Field, field_serializer
from bson import ObjectId


class MeetingCreate(BaseModel):
    title: str
    description: Optional[str] = None
    project_id: Optional[str] = None
    scheduled_at: datetime
    duration_minutes: Optional[int] = 60
    status: str = "scheduled"
    meeting_type: Optional[str] = None
    location: Optional[str] = None
    jitsi_room_name: Optional[str] = None
    jitsi_room_url: Optional[str] = None
    host_id: Optional[str] = None
    participant_ids: Optional[List[str]] = Field(default_factory=list)
    agenda: Optional[List[str]] = Field(default_factory=list)
    notes: Optional[str] = None
    action_items: Optional[List[str]] = Field(default_factory=list)


class MeetingUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    project_id: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    status: Optional[str] = None
    meeting_type: Optional[str] = None
    location: Optional[str] = None
    jitsi_room_name: Optional[str] = None
    jitsi_room_url: Optional[str] = None
    host_id: Optional[str] = None
    participant_ids: Optional[List[str]] = None
    agenda: Optional[List[str]] = None
    notes: Optional[str] = None
    action_items: Optional[List[str]] = None


class MeetingResponse(BaseModel):
    id: Any = Field(alias="_id")
    title: str
    description: Optional[str] = None
    project_id: Optional[Any] = None
    scheduled_at: datetime
    duration_minutes: Optional[int] = None
    status: str
    meeting_type: Optional[str] = None
    location: Optional[str] = None
    jitsi_room_name: Optional[str] = None
    jitsi_room_url: Optional[str] = None
    host_id: Optional[Any] = None
    participant_ids: Optional[List[Any]] = None
    agenda: Optional[List[str]] = None
    notes: Optional[str] = None
    action_items: Optional[List[str]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @field_serializer('id', 'project_id', 'host_id')
    def serialize_object_id(self, value: Any) -> Optional[str]:
        if isinstance(value, ObjectId):
            return str(value)
        return value
    
    @field_serializer('participant_ids')
    def serialize_participant_ids(self, value: Optional[List[Any]]) -> Optional[List[str]]:
        if value is None:
            return None
        return [str(item) if isinstance(item, ObjectId) else item for item in value]
    
    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True
