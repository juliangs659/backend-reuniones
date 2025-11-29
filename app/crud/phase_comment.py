"""CRUD operations for PhaseComment"""
from typing import Optional, List
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from app.schemas.phase_comment import PhaseCommentCreate, PhaseCommentUpdate


class PhaseCommentCRUD:
    """CRUD para gestionar comentarios en fases"""
    
    def __init__(self):
        self.collection_name = "phase_comments"
    
    async def create(
        self,
        db: AsyncIOMotorDatabase,
        comment_in: PhaseCommentCreate
    ) -> dict:
        """Crear nuevo comentario"""
        comment_dict = comment_in.model_dump()
        
        # Convertir IDs
        if "phase_id" in comment_dict and comment_dict["phase_id"]:
            comment_dict["phase_id"] = ObjectId(comment_dict["phase_id"])
        
        if "project_id" in comment_dict and comment_dict["project_id"]:
            comment_dict["project_id"] = ObjectId(comment_dict["project_id"])
        
        # Timestamps
        now = datetime.utcnow()
        comment_dict["created_at"] = now
        comment_dict["updated_at"] = now
        
        result = await db[self.collection_name].insert_one(comment_dict)
        created = await db[self.collection_name].find_one({"_id": result.inserted_id})
        return created
    
    async def get(
        self,
        db: AsyncIOMotorDatabase,
        comment_id: str
    ) -> Optional[dict]:
        """Obtener comentario por ID"""
        if not ObjectId.is_valid(comment_id):
            return None
        
        return await db[self.collection_name].find_one({"_id": ObjectId(comment_id)})
    
    async def get_multi(
        self,
        db: AsyncIOMotorDatabase,
        skip: int = 0,
        limit: int = 100,
        phase_id: Optional[str] = None,
        project_id: Optional[str] = None,
        user_email: Optional[str] = None
    ) -> List[dict]:
        """Listar comentarios con filtros"""
        query = {}
        
        if phase_id and ObjectId.is_valid(phase_id):
            query["phase_id"] = ObjectId(phase_id)
        
        if project_id and ObjectId.is_valid(project_id):
            query["project_id"] = ObjectId(project_id)
        
        if user_email:
            query["user_email"] = user_email
        
        cursor = db[self.collection_name].find(query).skip(skip).limit(limit).sort("created_at", -1)
        return await cursor.to_list(length=limit)
    
    async def get_by_phase(
        self,
        db: AsyncIOMotorDatabase,
        phase_id: str
    ) -> List[dict]:
        """Obtener todos los comentarios de una fase"""
        if not ObjectId.is_valid(phase_id):
            return []
        
        cursor = db[self.collection_name].find(
            {"phase_id": ObjectId(phase_id)}
        ).sort("created_at", 1)
        
        return await cursor.to_list(length=None)
    
    async def count(
        self,
        db: AsyncIOMotorDatabase,
        phase_id: Optional[str] = None,
        project_id: Optional[str] = None
    ) -> int:
        """Contar comentarios"""
        query = {}
        
        if phase_id and ObjectId.is_valid(phase_id):
            query["phase_id"] = ObjectId(phase_id)
        
        if project_id and ObjectId.is_valid(project_id):
            query["project_id"] = ObjectId(project_id)
        
        return await db[self.collection_name].count_documents(query)
    
    async def update(
        self,
        db: AsyncIOMotorDatabase,
        comment_id: str,
        comment_in: PhaseCommentUpdate
    ) -> Optional[dict]:
        """Actualizar comentario"""
        if not ObjectId.is_valid(comment_id):
            return None
        
        update_data = comment_in.model_dump(exclude_unset=True)
        if not update_data:
            return await self.get(db, comment_id)
        
        # Actualizar timestamp
        update_data["updated_at"] = datetime.utcnow()
        
        result = await db[self.collection_name].update_one(
            {"_id": ObjectId(comment_id)},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            return None
        
        return await self.get(db, comment_id)
    
    async def delete(
        self,
        db: AsyncIOMotorDatabase,
        comment_id: str
    ) -> bool:
        """Eliminar comentario"""
        if not ObjectId.is_valid(comment_id):
            return False
        
        result = await db[self.collection_name].delete_one({"_id": ObjectId(comment_id)})
        return result.deleted_count > 0


phase_comment_crud = PhaseCommentCRUD()
