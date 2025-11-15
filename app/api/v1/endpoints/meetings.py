from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.deps import get_db
from app.crud.meeting import meeting_crud
from app.schemas.meeting import MeetingCreate, MeetingUpdate, MeetingResponse
from app.schemas.common import PaginatedResponse, Message

router = APIRouter()


@router.post("/", response_model=MeetingResponse, status_code=201)
async def create_meeting(
    meeting_in: MeetingCreate,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    meeting_dict = await meeting_crud.create(db, meeting_in)
    return meeting_dict


@router.get("/", response_model=PaginatedResponse[MeetingResponse])
async def list_meetings(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    project_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    meetings = await meeting_crud.get_multi(
        db, 
        skip=skip, 
        limit=limit,
        project_id=project_id,
        status=status
    )
    total = await meeting_crud.count(db, project_id=project_id)
    
    return PaginatedResponse(
        items=meetings,
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )


@router.get("/{meeting_id}", response_model=MeetingResponse)
async def get_meeting(
    meeting_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    meeting = await meeting_crud.get(db, meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Reunión no encontrada")
    
    return meeting


@router.put("/{meeting_id}", response_model=MeetingResponse)
async def update_meeting(
    meeting_id: str,
    meeting_in: MeetingUpdate,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    meeting = await meeting_crud.get(db, meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Reunión no encontrada")
    
    updated_meeting = await meeting_crud.update(db, meeting_id, meeting_in)
    if not updated_meeting:
        raise HTTPException(status_code=400, detail="Error al actualizar la reunión")
    
    return updated_meeting


@router.delete("/{meeting_id}", response_model=Message)
async def delete_meeting(
    meeting_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    meeting = await meeting_crud.get(db, meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Reunión no encontrada")
    
    deleted = await meeting_crud.delete(db, meeting_id)
    if not deleted:
        raise HTTPException(status_code=400, detail="Error al eliminar la reunión")
    
    return Message(message="Reunión eliminada exitosamente")


@router.patch("/{meeting_id}/status", response_model=MeetingResponse)
async def update_meeting_status(
    meeting_id: str,
    status: str = Query(..., regex="^(scheduled|in_progress|completed|cancelled)$"),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    meeting = await meeting_crud.get(db, meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Reunión no encontrada")
    
    updated_meeting = await meeting_crud.update_status(db, meeting_id, status)
    if not updated_meeting:
        raise HTTPException(status_code=400, detail="Error al actualizar el estado")
    
    return updated_meeting
