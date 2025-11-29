"""Endpoints for Phase Comments"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.deps import get_db
from app.schemas.phase_comment import (
    PhaseCommentCreate,
    PhaseCommentUpdate,
    PhaseCommentResponse
)
from app.schemas.common import Message, PaginatedResponse
from app.crud.phase_comment import phase_comment_crud


router = APIRouter()


@router.post("/", response_model=PhaseCommentResponse, status_code=201)
async def create_comment(
    comment_in: PhaseCommentCreate,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Crear un nuevo comentario en una fase"""
    comment = await phase_comment_crud.create(db, comment_in)
    return comment


@router.get("/", response_model=PaginatedResponse[PhaseCommentResponse])
async def list_comments(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    phase_id: Optional[str] = Query(None),
    project_id: Optional[str] = Query(None),
    user_email: Optional[str] = Query(None),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Listar comentarios con filtros"""
    comments = await phase_comment_crud.get_multi(
        db,
        skip=skip,
        limit=limit,
        phase_id=phase_id,
        project_id=project_id,
        user_email=user_email
    )
    total = await phase_comment_crud.count(
        db,
        phase_id=phase_id,
        project_id=project_id
    )
    
    return PaginatedResponse(
        items=comments,
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )


@router.get("/phase/{phase_id}", response_model=list[PhaseCommentResponse])
async def get_phase_comments(
    phase_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Obtener todos los comentarios de una fase"""
    comments = await phase_comment_crud.get_by_phase(db, phase_id)
    return comments


@router.get("/{comment_id}", response_model=PhaseCommentResponse)
async def get_comment(
    comment_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Obtener comentario por ID"""
    comment = await phase_comment_crud.get(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")
    
    return comment


@router.put("/{comment_id}", response_model=PhaseCommentResponse)
async def update_comment(
    comment_id: str,
    comment_in: PhaseCommentUpdate,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Actualizar comentario"""
    comment = await phase_comment_crud.get(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")
    
    updated = await phase_comment_crud.update(db, comment_id, comment_in)
    if not updated:
        raise HTTPException(status_code=400, detail="Error al actualizar")
    
    return updated


@router.delete("/{comment_id}", response_model=Message)
async def delete_comment(
    comment_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Eliminar comentario"""
    comment = await phase_comment_crud.get(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")
    
    deleted = await phase_comment_crud.delete(db, comment_id)
    if not deleted:
        raise HTTPException(status_code=400, detail="Error al eliminar")
    
    return Message(message="Comentario eliminado exitosamente")
