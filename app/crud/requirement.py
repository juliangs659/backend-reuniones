"""CRUD operations for Requirement"""
from typing import Optional, List
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from app.schemas.requirement import RequirementCreate, RequirementUpdate


class RequirementCRUD:
    """CRUD para gestionar requerimientos"""
    
    def __init__(self):
        self.collection_name = "requirements"
    
    async def create(
        self,
        db: AsyncIOMotorDatabase,
        requirement_in: RequirementCreate
    ) -> dict:
        """Crear nuevo requerimiento"""
        req_dict = requirement_in.model_dump()
        
        # Convertir IDs
        if "project_id" in req_dict and req_dict["project_id"]:
            req_dict["project_id"] = ObjectId(req_dict["project_id"])
        
        if "phase_id" in req_dict and req_dict["phase_id"]:
            req_dict["phase_id"] = ObjectId(req_dict["phase_id"])
        
        if "transcription_id" in req_dict and req_dict["transcription_id"]:
            req_dict["transcription_id"] = ObjectId(req_dict["transcription_id"])
        
        # Timestamps y defaults
        now = datetime.utcnow()
        req_dict["created_at"] = now
        req_dict["updated_at"] = now
        req_dict["extracted_by_ai"] = req_dict.get("extracted_by_ai", False)
        req_dict["user_edited"] = False
        
        result = await db[self.collection_name].insert_one(req_dict)
        created = await db[self.collection_name].find_one({"_id": result.inserted_id})
        return created
    
    async def get(
        self,
        db: AsyncIOMotorDatabase,
        requirement_id: str
    ) -> Optional[dict]:
        """Obtener requerimiento por ID"""
        if not ObjectId.is_valid(requirement_id):
            return None
        
        return await db[self.collection_name].find_one({"_id": ObjectId(requirement_id)})
    
    async def get_multi(
        self,
        db: AsyncIOMotorDatabase,
        skip: int = 0,
        limit: int = 100,
        project_id: Optional[str] = None,
        phase_id: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        type: Optional[str] = None
    ) -> List[dict]:
        """Listar requerimientos con filtros"""
        query = {}
        
        if project_id and ObjectId.is_valid(project_id):
            query["project_id"] = ObjectId(project_id)
        
        if phase_id and ObjectId.is_valid(phase_id):
            query["phase_id"] = ObjectId(phase_id)
        
        if status:
            query["status"] = status
        
        if priority:
            query["priority"] = priority
        
        if type:
            query["type"] = type
        
        cursor = db[self.collection_name].find(query).skip(skip).limit(limit).sort("created_at", -1)
        return await cursor.to_list(length=limit)
    
    async def get_by_phase(
        self,
        db: AsyncIOMotorDatabase,
        phase_id: str
    ) -> List[dict]:
        """Obtener todos los requerimientos de una fase"""
        if not ObjectId.is_valid(phase_id):
            return []
        
        cursor = db[self.collection_name].find(
            {"phase_id": ObjectId(phase_id)}
        ).sort("created_at", 1)
        
        return await cursor.to_list(length=None)
    
    async def count(
        self,
        db: AsyncIOMotorDatabase,
        project_id: Optional[str] = None,
        phase_id: Optional[str] = None,
        status: Optional[str] = None
    ) -> int:
        """Contar requerimientos"""
        query = {}
        
        if project_id and ObjectId.is_valid(project_id):
            query["project_id"] = ObjectId(project_id)
        
        if phase_id and ObjectId.is_valid(phase_id):
            query["phase_id"] = ObjectId(phase_id)
        
        if status:
            query["status"] = status
        
        return await db[self.collection_name].count_documents(query)
    
    async def update(
        self,
        db: AsyncIOMotorDatabase,
        requirement_id: str,
        requirement_in: RequirementUpdate
    ) -> Optional[dict]:
        """Actualizar requerimiento"""
        if not ObjectId.is_valid(requirement_id):
            return None
        
        update_data = requirement_in.model_dump(exclude_unset=True)
        if not update_data:
            return await self.get(db, requirement_id)
        
        # Convertir IDs si existen
        if "phase_id" in update_data and update_data["phase_id"]:
            update_data["phase_id"] = ObjectId(update_data["phase_id"])
        
        # Marcar como editado por usuario
        if any(key in update_data for key in ["title", "description", "priority", "type"]):
            update_data["user_edited"] = True
        
        # Actualizar timestamp
        update_data["updated_at"] = datetime.utcnow()
        
        result = await db[self.collection_name].update_one(
            {"_id": ObjectId(requirement_id)},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            return None
        
        return await self.get(db, requirement_id)
    
    async def delete(
        self,
        db: AsyncIOMotorDatabase,
        requirement_id: str
    ) -> bool:
        """Eliminar requerimiento"""
        if not ObjectId.is_valid(requirement_id):
            return False
        
        result = await db[self.collection_name].delete_one({"_id": ObjectId(requirement_id)})
        return result.deleted_count > 0
    
    async def update_status(
        self,
        db: AsyncIOMotorDatabase,
        requirement_id: str,
        status: str
    ) -> Optional[dict]:
        """Actualizar solo el estado del requerimiento"""
        if not ObjectId.is_valid(requirement_id):
            return None
        
        await db[self.collection_name].update_one(
            {"_id": ObjectId(requirement_id)},
            {"$set": {"status": status, "updated_at": datetime.utcnow()}}
        )
        
        return await self.get(db, requirement_id)
    
    async def move_to_phase(
        self,
        db: AsyncIOMotorDatabase,
        requirement_id: str,
        new_phase_id: str
    ) -> Optional[dict]:
        """Mover requerimiento a otra fase"""
        if not ObjectId.is_valid(requirement_id) or not ObjectId.is_valid(new_phase_id):
            return None
        
        await db[self.collection_name].update_one(
            {"_id": ObjectId(requirement_id)},
            {"$set": {
                "phase_id": ObjectId(new_phase_id),
                "updated_at": datetime.utcnow()
            }}
        )
        
        return await self.get(db, requirement_id)


requirement_crud = RequirementCRUD()
