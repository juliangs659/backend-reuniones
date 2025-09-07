"""Schemas module - Esquemas Pydantic para validación de datos"""

from app.schemas.user import User, UserCreate, UserUpdate, UserInDB
from app.schemas.client import Client, ClientCreate, ClientUpdate, ClientInDB
from app.schemas.project import Project, ProjectCreate, ProjectUpdate, ProjectInDB
from app.schemas.meeting import Meeting, MeetingCreate, MeetingUpdate, MeetingInDB
from app.schemas.transcription import Transcription, TranscriptionCreate, TranscriptionUpdate, TranscriptionInDB
from app.schemas.chat_message import ChatMessage, ChatMessageCreate, ChatMessageUpdate, ChatMessageInDB
from app.schemas.auth import Token, TokenData, LoginRequest
from app.schemas.common import Message, ErrorResponse

__all__ = [
    # User schemas
    "User", "UserCreate", "UserUpdate", "UserInDB",
    # Client schemas
    "Client", "ClientCreate", "ClientUpdate", "ClientInDB",
    # Project schemas
    "Project", "ProjectCreate", "ProjectUpdate", "ProjectInDB",
    # Meeting schemas
    "Meeting", "MeetingCreate", "MeetingUpdate", "MeetingInDB",
    # Transcription schemas
    "Transcription", "TranscriptionCreate", "TranscriptionUpdate", "TranscriptionInDB",
    # Chat message schemas
    "ChatMessage", "ChatMessageCreate", "ChatMessageUpdate", "ChatMessageInDB",
    # Auth schemas
    "Token", "TokenData", "LoginRequest",
    # Common schemas
    "Message", "ErrorResponse"
]