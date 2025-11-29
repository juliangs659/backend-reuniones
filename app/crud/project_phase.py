"""CRUD operations for ProjectPhase"""
from typing import Optional, List
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from app.schemas.project_phase import ProjectPhaseCreate, ProjectPhaseUpdate


class ProjectPhaseCRUD:
    """CRUD para gestionar fases de proyectos"""
    
    def __init__(self):
        self.collection_name = "project_phases"
    
    async def create(
        self,
        db: AsyncIOMotorDatabase,
        phase_in: ProjectPhaseCreate
    ) -> dict:
        """Crear nueva fase"""
        phase_dict = phase_in.model_dump()
        
        # Convertir project_id
        if "project_id" in phase_dict and phase_dict["project_id"]:
            phase_dict["project_id"] = ObjectId(phase_dict["project_id"])
        
        # Timestamps
        now = datetime.utcnow()
        phase_dict["created_at"] = now
        phase_dict["updated_at"] = now
        phase_dict["completion_percentage"] = 0
        
        result = await db[self.collection_name].insert_one(phase_dict)
        created = await db[self.collection_name].find_one({"_id": result.inserted_id})
        return created
    
    async def get(
        self,
        db: AsyncIOMotorDatabase,
        phase_id: str
    ) -> Optional[dict]:
        """Obtener fase por ID"""
        if not ObjectId.is_valid(phase_id):
            return None
        
        return await db[self.collection_name].find_one({"_id": ObjectId(phase_id)})
    
    async def get_multi(
        self,
        db: AsyncIOMotorDatabase,
        skip: int = 0,
        limit: int = 100,
        project_id: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[dict]:
        """Listar fases con filtros"""
        query = {}
        
        if project_id and ObjectId.is_valid(project_id):
            query["project_id"] = ObjectId(project_id)
        
        if status:
            query["status"] = status
        
        cursor = db[self.collection_name].find(query).skip(skip).limit(limit).sort("order", 1)
        return await cursor.to_list(length=limit)
    
    async def get_by_project(
        self,
        db: AsyncIOMotorDatabase,
        project_id: str
    ) -> List[dict]:
        """Obtener todas las fases de un proyecto ordenadas"""
        if not ObjectId.is_valid(project_id):
            return []
        
        cursor = db[self.collection_name].find(
            {"project_id": ObjectId(project_id)}
        ).sort("order", 1)
        
        return await cursor.to_list(length=None)
    
    async def count(
        self,
        db: AsyncIOMotorDatabase,
        project_id: Optional[str] = None,
        status: Optional[str] = None
    ) -> int:
        """Contar fases"""
        query = {}
        
        if project_id and ObjectId.is_valid(project_id):
            query["project_id"] = ObjectId(project_id)
        
        if status:
            query["status"] = status
        
        return await db[self.collection_name].count_documents(query)
    
    async def update(
        self,
        db: AsyncIOMotorDatabase,
        phase_id: str,
        phase_in: ProjectPhaseUpdate
    ) -> Optional[dict]:
        """Actualizar fase"""
        if not ObjectId.is_valid(phase_id):
            return None
        
        update_data = phase_in.model_dump(exclude_unset=True)
        if not update_data:
            return await self.get(db, phase_id)
        
        # Actualizar timestamp
        update_data["updated_at"] = datetime.utcnow()
        
        result = await db[self.collection_name].update_one(
            {"_id": ObjectId(phase_id)},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            return None
        
        return await self.get(db, phase_id)
    
    async def delete(
        self,
        db: AsyncIOMotorDatabase,
        phase_id: str
    ) -> bool:
        """Eliminar fase"""
        if not ObjectId.is_valid(phase_id):
            return False
        
        result = await db[self.collection_name].delete_one({"_id": ObjectId(phase_id)})
        return result.deleted_count > 0
    
    async def reorder_phases(
        self,
        db: AsyncIOMotorDatabase,
        project_id: str,
        phase_orders: List[dict]
    ) -> bool:
        """
        Reordenar fases del proyecto.
        phase_orders: [{"phase_id": "xxx", "order": 1}, ...]
        """
        if not ObjectId.is_valid(project_id):
            return False
        
        for item in phase_orders:
            # Manejar tanto dict como objeto Pydantic
            if hasattr(item, 'phase_id'):
                phase_id = item.phase_id
                new_order = item.order
            else:
                phase_id = item.get("phase_id")
                new_order = item.get("order")
            
            if phase_id and ObjectId.is_valid(phase_id) and new_order is not None:
                await db[self.collection_name].update_one(
                    {"_id": ObjectId(phase_id), "project_id": ObjectId(project_id)},
                    {"$set": {"order": new_order, "updated_at": datetime.utcnow()}}
                )
        
        return True
    
    async def update_status(
        self,
        db: AsyncIOMotorDatabase,
        phase_id: str,
        status: str
    ) -> Optional[dict]:
        """Actualizar solo el estado de la fase"""
        if not ObjectId.is_valid(phase_id):
            return None
        
        update_data = {
            "status": status,
            "updated_at": datetime.utcnow()
        }
        
        # Si se marca como completada, agregar fecha
        if status == "completed":
            update_data["actual_end_date"] = datetime.utcnow()
            update_data["completion_percentage"] = 100
        
        # Si se inicia, agregar fecha de inicio
        if status == "in_progress":
            phase = await self.get(db, phase_id)
            if phase and not phase.get("actual_start_date"):
                update_data["actual_start_date"] = datetime.utcnow()
        
        await db[self.collection_name].update_one(
            {"_id": ObjectId(phase_id)},
            {"$set": update_data}
        )
        
        return await self.get(db, phase_id)
    
    async def update_completion(
        self,
        db: AsyncIOMotorDatabase,
        phase_id: str,
        completion_percentage: int
    ) -> Optional[dict]:
        """Actualizar porcentaje de completitud"""
        if not ObjectId.is_valid(phase_id):
            return None
        
        if completion_percentage < 0 or completion_percentage > 100:
            return None
        
        await db[self.collection_name].update_one(
            {"_id": ObjectId(phase_id)},
            {"$set": {
                "completion_percentage": completion_percentage,
                "updated_at": datetime.utcnow()
            }}
        )
        
        return await self.get(db, phase_id)


project_phase_crud = ProjectPhaseCRUD()
