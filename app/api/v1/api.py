from fastapi import APIRouter
from app.api.v1.endpoints import (
    meetings_router,
    transcriptions,
    project_phases,
    requirements,
    phase_comments
)

api_router = APIRouter()

# Meetings
api_router.include_router(
    meetings_router, 
    prefix="/meetings", 
    tags=["meetings"]
)

# Transcripciones
api_router.include_router(
    transcriptions.router,
    prefix="/transcriptions",
    tags=["transcriptions"]
)

# Fases de Proyectos
api_router.include_router(
    project_phases.router,
    prefix="/project-phases",
    tags=["project-phases"]
)

# Requerimientos
api_router.include_router(
    requirements.router,
    prefix="/requirements",
    tags=["requirements"]
)

# Comentarios de Fases
api_router.include_router(
    phase_comments.router,
    prefix="/phase-comments",
    tags=["phase-comments"]
)
