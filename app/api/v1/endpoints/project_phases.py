"""Endpoints for Project Phases"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Body
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.deps import get_db
from app.schemas.project_phase import (
    ProjectPhaseCreate,
    ProjectPhaseUpdate,
    ProjectPhaseResponse,
    PhaseReorderRequest
)
from app.schemas.common import Message, PaginatedResponse
from app.crud.project_phase import project_phase_crud


router = APIRouter()


@router.post("/", response_model=ProjectPhaseResponse, status_code=201)
async def create_phase(
    phase_in: ProjectPhaseCreate,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Crear una nueva fase en el proyecto"""
    phase = await project_phase_crud.create(db, phase_in)
    return phase


@router.get("/", response_model=PaginatedResponse[ProjectPhaseResponse])
async def list_phases(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    project_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Listar fases con filtros"""
    phases = await project_phase_crud.get_multi(
        db,
        skip=skip,
        limit=limit,
        project_id=project_id,
        status=status
    )
    total = await project_phase_crud.count(db, project_id=project_id, status=status)
    
    return PaginatedResponse(
        items=phases,
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )


@router.get("/project/{project_id}", response_model=list[ProjectPhaseResponse])
async def get_project_phases(
    project_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Obtener todas las fases de un proyecto ordenadas"""
    phases = await project_phase_crud.get_by_project(db, project_id)
    return phases


@router.get("/{phase_id}", response_model=ProjectPhaseResponse)
async def get_phase(
    phase_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Obtener fase por ID"""
    phase = await project_phase_crud.get(db, phase_id)
    if not phase:
        raise HTTPException(status_code=404, detail="Fase no encontrada")
    
    return phase


@router.put("/{phase_id}", response_model=ProjectPhaseResponse)
async def update_phase(
    phase_id: str,
    phase_in: ProjectPhaseUpdate,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Actualizar fase"""
    phase = await project_phase_crud.get(db, phase_id)
    if not phase:
        raise HTTPException(status_code=404, detail="Fase no encontrada")
    
    updated = await project_phase_crud.update(db, phase_id, phase_in)
    if not updated:
        raise HTTPException(status_code=400, detail="Error al actualizar")
    
    return updated


@router.delete("/{phase_id}", response_model=Message)
async def delete_phase(
    phase_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Eliminar fase"""
    phase = await project_phase_crud.get(db, phase_id)
    if not phase:
        raise HTTPException(status_code=404, detail="Fase no encontrada")
    
    deleted = await project_phase_crud.delete(db, phase_id)
    if not deleted:
        raise HTTPException(status_code=400, detail="Error al eliminar")
    
    return Message(message="Fase eliminada exitosamente")


@router.patch("/{phase_id}/status", response_model=ProjectPhaseResponse)
async def update_phase_status(
    phase_id: str,
    status: str = Query(..., regex="^(pending|in_progress|completed|blocked)$"),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Actualizar estado de la fase"""
    phase = await project_phase_crud.get(db, phase_id)
    if not phase:
        raise HTTPException(status_code=404, detail="Fase no encontrada")
    
    updated = await project_phase_crud.update_status(db, phase_id, status)
    if not updated:
        raise HTTPException(status_code=400, detail="Error al actualizar estado")
    
    return updated


@router.patch("/{phase_id}/completion", response_model=ProjectPhaseResponse)
async def update_phase_completion(
    phase_id: str,
    completion: int = Query(..., ge=0, le=100),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Actualizar porcentaje de completitud de la fase"""
    phase = await project_phase_crud.get(db, phase_id)
    if not phase:
        raise HTTPException(status_code=404, detail="Fase no encontrada")
    
    updated = await project_phase_crud.update_completion(db, phase_id, completion)
    if not updated:
        raise HTTPException(status_code=400, detail="Error al actualizar completitud")
    
    return updated


@router.post("/reorder", response_model=Message)
async def reorder_phases(
    project_id: str = Query(..., description="ID del proyecto"),
    reorder_data: PhaseReorderRequest = Body(...),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Reordenar fases del proyecto.
    
    Ejemplo de body:
    {
        "phase_orders": [
            {"phase_id": "xxx", "order": 1},
            {"phase_id": "yyy", "order": 2}
        ]
    }
    """
    success = await project_phase_crud.reorder_phases(
        db,
        project_id,
        reorder_data.phase_orders
    )
    
    if not success:
        raise HTTPException(status_code=400, detail="Error al reordenar fases")
    
    return Message(message="Fases reordenadas exitosamente")
