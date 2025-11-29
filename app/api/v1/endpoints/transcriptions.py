"""Endpoints for Transcriptions"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.deps import get_db
from app.schemas.transcription import (
    TranscriptionCreate,
    TranscriptionUpdate,
    TranscriptionResponse,
    TranscriptionProcessRequest
)
from app.schemas.common import Message, PaginatedResponse
from app.crud.transcription import transcription_crud


router = APIRouter()


@router.post("/", response_model=TranscriptionResponse, status_code=201)
async def create_transcription(
    transcription_in: TranscriptionCreate,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Crear una nueva transcripción (carga manual desde Teams)"""
    transcription = await transcription_crud.create(db, transcription_in)
    return transcription


@router.get("/", response_model=PaginatedResponse[TranscriptionResponse])
async def list_transcriptions(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    user_email: Optional[str] = Query(None),
    project_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Listar transcripciones con filtros"""
    transcriptions = await transcription_crud.get_multi(
        db,
        skip=skip,
        limit=limit,
        user_email=user_email,
        project_id=project_id,
        status=status
    )
    total = await transcription_crud.count(
        db,
        user_email=user_email,
        project_id=project_id,
        status=status
    )
    
    return PaginatedResponse(
        items=transcriptions,
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )


@router.get("/{transcription_id}", response_model=TranscriptionResponse)
async def get_transcription(
    transcription_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Obtener transcripción por ID"""
    transcription = await transcription_crud.get(db, transcription_id)
    if not transcription:
        raise HTTPException(status_code=404, detail="Transcripción no encontrada")
    
    return transcription


@router.put("/{transcription_id}", response_model=TranscriptionResponse)
async def update_transcription(
    transcription_id: str,
    transcription_in: TranscriptionUpdate,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Actualizar transcripción"""
    transcription = await transcription_crud.get(db, transcription_id)
    if not transcription:
        raise HTTPException(status_code=404, detail="Transcripción no encontrada")
    
    updated = await transcription_crud.update(db, transcription_id, transcription_in)
    if not updated:
        raise HTTPException(status_code=400, detail="Error al actualizar")
    
    return updated


@router.delete("/{transcription_id}", response_model=Message)
async def delete_transcription(
    transcription_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Eliminar transcripción"""
    transcription = await transcription_crud.get(db, transcription_id)
    if not transcription:
        raise HTTPException(status_code=404, detail="Transcripción no encontrada")
    
    deleted = await transcription_crud.delete(db, transcription_id)
    if not deleted:
        raise HTTPException(status_code=400, detail="Error al eliminar")
    
    return Message(message="Transcripción eliminada exitosamente")


@router.post("/{transcription_id}/process", response_model=TranscriptionResponse)
async def process_transcription_with_ai(
    transcription_id: str,
    process_request: TranscriptionProcessRequest,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Procesar transcripción con IA (OpenAI).
    
    Extrae:
    - Resumen ejecutivo
    - Fases del proyecto
    - Requerimientos funcionales y no funcionales
    - Decisiones técnicas
    - Acciones pendientes
    
    Si la transcripción tiene un project_id asociado, automáticamente:
    - Crea las fases identificadas en el proyecto
    - Crea los requerimientos extraídos y los asigna a las fases
    """
    transcription = await transcription_crud.get(db, transcription_id)
    if not transcription:
        raise HTTPException(status_code=404, detail="Transcripción no encontrada")
    
    if transcription.get("status") == "processing":
        raise HTTPException(
            status_code=400,
            detail="La transcripción ya está siendo procesada"
        )
    
    try:
        processed = await transcription_crud.process_with_ai(
            db,
            transcription_id,
            project_context=process_request.project_context
        )
        
        if not processed:
            raise HTTPException(status_code=500, detail="Error al procesar con IA")
        
        return processed
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar transcripción: {str(e)}"
        )
