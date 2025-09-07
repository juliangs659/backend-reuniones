from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    projects,
    clients,
    meetings,
    transcriptions,
    ai_chat,
    users
)

api_router = APIRouter()

# Incluir todas las rutas
api_router.include_router(
    auth.router, 
    prefix="/auth", 
    tags=["authentication"]
)

api_router.include_router(
    users.router, 
    prefix="/users", 
    tags=["users"]
)

api_router.include_router(
    projects.router, 
    prefix="/projects", 
    tags=["projects"]
)

api_router.include_router(
    clients.router, 
    prefix="/clients", 
    tags=["clients"]
)

api_router.include_router(
    meetings.router, 
    prefix="/meetings", 
    tags=["meetings"]
)

api_router.include_router(
    transcriptions.router, 
    prefix="/transcriptions", 
    tags=["transcriptions"]
)

api_router.include_router(
    ai_chat.router, 
    prefix="/ai", 
    tags=["ai-chat"]
)