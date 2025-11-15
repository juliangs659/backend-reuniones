"""Endpoints for Requirements"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.deps import get_db
from app.schemas.requirement import (
    RequirementCreate,
    RequirementUpdate,
    RequirementResponse
)
from app.schemas.common import Message, PaginatedResponse
from app.crud.requirement import requirement_crud


router = APIRouter()


@router.post("/", response_model=RequirementResponse, status_code=201)
async def create_requirement(
    requirement_in: RequirementCreate,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Crear un nuevo requerimiento"""
    requirement = await requirement_crud.create(db, requirement_in)
    return requirement


@router.get("/", response_model=PaginatedResponse[RequirementResponse])
async def list_requirements(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    project_id: Optional[str] = Query(None),
    phase_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Listar requerimientos con filtros"""
    requirements = await requirement_crud.get_multi(
        db,
        skip=skip,
        limit=limit,
        project_id=project_id,
        phase_id=phase_id,
        status=status,
        priority=priority,
        type=type
    )
    total = await requirement_crud.count(
        db,
        project_id=project_id,
        phase_id=phase_id,
        status=status
    )
    
    return PaginatedResponse(
        items=requirements,
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )


@router.get("/phase/{phase_id}", response_model=list[RequirementResponse])
async def get_phase_requirements(
    phase_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Obtener todos los requerimientos de una fase"""
    requirements = await requirement_crud.get_by_phase(db, phase_id)
    return requirements


@router.get("/{requirement_id}", response_model=RequirementResponse)
async def get_requirement(
    requirement_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Obtener requerimiento por ID"""
    requirement = await requirement_crud.get(db, requirement_id)
    if not requirement:
        raise HTTPException(status_code=404, detail="Requerimiento no encontrado")
    
    return requirement


@router.put("/{requirement_id}", response_model=RequirementResponse)
async def update_requirement(
    requirement_id: str,
    requirement_in: RequirementUpdate,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Actualizar requerimiento"""
    requirement = await requirement_crud.get(db, requirement_id)
    if not requirement:
        raise HTTPException(status_code=404, detail="Requerimiento no encontrado")
    
    updated = await requirement_crud.update(db, requirement_id, requirement_in)
    if not updated:
        raise HTTPException(status_code=400, detail="Error al actualizar")
    
    return updated


@router.delete("/{requirement_id}", response_model=Message)
async def delete_requirement(
    requirement_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Eliminar requerimiento"""
    requirement = await requirement_crud.get(db, requirement_id)
    if not requirement:
        raise HTTPException(status_code=404, detail="Requerimiento no encontrado")
    
    deleted = await requirement_crud.delete(db, requirement_id)
    if not deleted:
        raise HTTPException(status_code=400, detail="Error al eliminar")
    
    return Message(message="Requerimiento eliminado exitosamente")


@router.patch("/{requirement_id}/status", response_model=RequirementResponse)
async def update_requirement_status(
    requirement_id: str,
    status: str = Query(..., regex="^(pending|in_progress|completed|rejected)$"),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Actualizar estado del requerimiento"""
    requirement = await requirement_crud.get(db, requirement_id)
    if not requirement:
        raise HTTPException(status_code=404, detail="Requerimiento no encontrado")
    
    updated = await requirement_crud.update_status(db, requirement_id, status)
    if not updated:
        raise HTTPException(status_code=400, detail="Error al actualizar estado")
    
    return updated


@router.patch("/{requirement_id}/move", response_model=RequirementResponse)
async def move_requirement_to_phase(
    requirement_id: str,
    new_phase_id: str = Query(..., description="ID de la nueva fase"),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Mover requerimiento a otra fase"""
    requirement = await requirement_crud.get(db, requirement_id)
    if not requirement:
        raise HTTPException(status_code=404, detail="Requerimiento no encontrado")
    
    updated = await requirement_crud.move_to_phase(db, requirement_id, new_phase_id)
    if not updated:
        raise HTTPException(status_code=400, detail="Error al mover requerimiento")
    
    return updated
