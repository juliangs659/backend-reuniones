"""CRUD operations for Transcription"""
from typing import Optional, List
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from app.schemas.transcription import TranscriptionCreate, TranscriptionUpdate
from app.services.openai_service import openai_service


class TranscriptionCRUD:
    """CRUD para gestionar transcripciones"""
    
    def __init__(self):
        self.collection_name = "transcriptions"
    
    async def create(
        self, 
        db: AsyncIOMotorDatabase, 
        transcription_in: TranscriptionCreate
    ) -> dict:
        """Crear una nueva transcripción"""
        transcription_dict = transcription_in.model_dump()
        
        # Convertir IDs
        if "meeting_id" in transcription_dict and transcription_dict["meeting_id"]:
            transcription_dict["meeting_id"] = ObjectId(transcription_dict["meeting_id"])
        
        if "project_id" in transcription_dict and transcription_dict["project_id"]:
            transcription_dict["project_id"] = ObjectId(transcription_dict["project_id"])
        
        # Agregar timestamps y estado inicial
        now = datetime.utcnow()
        transcription_dict["created_at"] = now
        transcription_dict["updated_at"] = now
        transcription_dict["status"] = "pending"
        
        result = await db[self.collection_name].insert_one(transcription_dict)
        created = await db[self.collection_name].find_one({"_id": result.inserted_id})
        return created
    
    async def get(
        self, 
        db: AsyncIOMotorDatabase, 
        transcription_id: str
    ) -> Optional[dict]:
        """Obtener transcripción por ID"""
        if not ObjectId.is_valid(transcription_id):
            return None
        
        return await db[self.collection_name].find_one({"_id": ObjectId(transcription_id)})
    
    async def get_multi(
        self,
        db: AsyncIOMotorDatabase,
        skip: int = 0,
        limit: int = 10,
        user_email: Optional[str] = None,
        project_id: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[dict]:
        """Listar transcripciones con filtros"""
        query = {}
        
        if user_email:
            query["user_email"] = user_email
        
        if project_id and ObjectId.is_valid(project_id):
            query["project_id"] = ObjectId(project_id)
        
        if status:
            query["status"] = status
        
        cursor = db[self.collection_name].find(query).skip(skip).limit(limit).sort("created_at", -1)
        return await cursor.to_list(length=limit)
    
    async def count(
        self,
        db: AsyncIOMotorDatabase,
        user_email: Optional[str] = None,
        project_id: Optional[str] = None,
        status: Optional[str] = None
    ) -> int:
        """Contar transcripciones"""
        query = {}
        
        if user_email:
            query["user_email"] = user_email
        
        if project_id and ObjectId.is_valid(project_id):
            query["project_id"] = ObjectId(project_id)
        
        if status:
            query["status"] = status
        
        return await db[self.collection_name].count_documents(query)
    
    async def update(
        self,
        db: AsyncIOMotorDatabase,
        transcription_id: str,
        transcription_in: TranscriptionUpdate
    ) -> Optional[dict]:
        """Actualizar transcripción"""
        if not ObjectId.is_valid(transcription_id):
            return None
        
        update_data = transcription_in.model_dump(exclude_unset=True)
        if not update_data:
            return await self.get(db, transcription_id)
        
        # Convertir IDs si existen
        if "meeting_id" in update_data and update_data["meeting_id"]:
            update_data["meeting_id"] = ObjectId(update_data["meeting_id"])
        
        if "project_id" in update_data and update_data["project_id"]:
            update_data["project_id"] = ObjectId(update_data["project_id"])
        
        # Actualizar timestamp
        update_data["updated_at"] = datetime.utcnow()
        
        result = await db[self.collection_name].update_one(
            {"_id": ObjectId(transcription_id)},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            return None
        
        return await self.get(db, transcription_id)
    
    async def delete(
        self,
        db: AsyncIOMotorDatabase,
        transcription_id: str
    ) -> bool:
        """Eliminar transcripción"""
        if not ObjectId.is_valid(transcription_id):
            return False
        
        result = await db[self.collection_name].delete_one({"_id": ObjectId(transcription_id)})
        return result.deleted_count > 0
    
    async def process_with_ai(
        self,
        db: AsyncIOMotorDatabase,
        transcription_id: str,
        project_context: Optional[str] = None
    ) -> Optional[dict]:
        """
        Procesar transcripción con OpenAI para extraer requerimientos y fases.
        
        Este método:
        1. Obtiene la transcripción
        2. La procesa con OpenAI
        3. Guarda el análisis en ai_analysis
        4. Crea las fases del proyecto automáticamente
        5. Crea los requerimientos extraídos
        """
        if not ObjectId.is_valid(transcription_id):
            return None
        
        # Obtener transcripción
        transcription = await self.get(db, transcription_id)
        if not transcription:
            return None
        
        try:
            # Actualizar estado a processing
            await db[self.collection_name].update_one(
                {"_id": ObjectId(transcription_id)},
                {"$set": {"status": "processing", "updated_at": datetime.utcnow()}}
            )
            
            # Procesar con OpenAI
            ai_result = await openai_service.analyze_transcription(
                transcription_text=transcription["transcription_text"],
                project_context=project_context
            )
            
            # Guardar resultado del análisis
            update_data = {
                "ai_analysis": ai_result,
                "status": "completed",
                "processed_at": datetime.utcnow(),
                "ai_model_used": openai_service.model,
                "updated_at": datetime.utcnow()
            }
            
            await db[self.collection_name].update_one(
                {"_id": ObjectId(transcription_id)},
                {"$set": update_data}
            )
            
            # Si hay project_id, crear fases y requerimientos automáticamente
            if transcription.get("project_id"):
                await self._create_phases_and_requirements(
                    db=db,
                    project_id=transcription["project_id"],
                    transcription_id=ObjectId(transcription_id),
                    ai_result=ai_result
                )
            
            return await self.get(db, transcription_id)
            
        except Exception as e:
            # Guardar error
            await db[self.collection_name].update_one(
                {"_id": ObjectId(transcription_id)},
                {
                    "$set": {
                        "status": "error",
                        "error_message": str(e),
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            raise
    
    async def _create_phases_and_requirements(
        self,
        db: AsyncIOMotorDatabase,
        project_id: ObjectId,
        transcription_id: ObjectId,
        ai_result: dict
    ):
        """Crear fases y requerimientos extraídos por IA"""
        now = datetime.utcnow()
        
        # Crear fases
        phases_created = {}
        for phase_data in ai_result.get("phases", []):
            phase_doc = {
                "project_id": project_id,
                "name": phase_data["name"],
                "description": phase_data.get("description", ""),
                "status": "pending",
                "order": phase_data.get("order", 1),
                "completion_percentage": 0,
                "created_at": now,
                "updated_at": now
            }
            
            result = await db["project_phases"].insert_one(phase_doc)
            phases_created[phase_data["name"]] = result.inserted_id
        
        # Crear requerimientos
        for req_data in ai_result.get("requirements", []):
            # Buscar fase correspondiente
            phase_name = req_data.get("phase", "")
            phase_id = phases_created.get(phase_name)
            
            # Si no se encuentra la fase, usar la primera creada o None
            if not phase_id and phases_created:
                phase_id = list(phases_created.values())[0]
            
            if phase_id:
                req_doc = {
                    "project_id": project_id,
                    "phase_id": phase_id,
                    "transcription_id": transcription_id,
                    "title": req_data["title"],
                    "description": req_data.get("description", ""),
                    "type": req_data.get("type", "functional"),
                    "priority": req_data.get("priority", "medium"),
                    "status": "pending",
                    "extracted_by_ai": True,
                    "user_edited": False,
                    "created_at": now,
                    "updated_at": now
                }
                
                await db["requirements"].insert_one(req_doc)


transcription_crud = TranscriptionCRUD()
