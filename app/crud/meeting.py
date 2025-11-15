from typing import Optional, List
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime

from app.schemas.meeting import MeetingCreate, MeetingUpdate


class MeetingCRUD:
    def __init__(self):
        self.collection_name = "meetings"
    
    async def get(self, db: AsyncIOMotorDatabase, meeting_id: str) -> Optional[dict]:
        if not ObjectId.is_valid(meeting_id):
            return None
        
        meeting_data = await db[self.collection_name].find_one({"_id": ObjectId(meeting_id)})
        return meeting_data
    
    async def get_multi(
        self, 
        db: AsyncIOMotorDatabase, 
        skip: int = 0, 
        limit: int = 100,
        project_id: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[dict]:
        query = {}
        if project_id and ObjectId.is_valid(project_id):
            query["project_id"] = ObjectId(project_id)
        if status:
            query["status"] = status
        
        cursor = db[self.collection_name].find(query).sort("scheduled_at", -1).skip(skip).limit(limit)
        meetings = []
        async for meeting_data in cursor:
            meetings.append(meeting_data)
        return meetings
    
    async def count(self, db: AsyncIOMotorDatabase, project_id: Optional[str] = None) -> int:
        query = {}
        if project_id and ObjectId.is_valid(project_id):
            query["project_id"] = ObjectId(project_id)
        return await db[self.collection_name].count_documents(query)
    
    async def create(self, db: AsyncIOMotorDatabase, meeting_in: MeetingCreate) -> dict:
        from datetime import datetime
        
        meeting_dict = meeting_in.model_dump()
        
        if "project_id" in meeting_dict and meeting_dict["project_id"]:
            meeting_dict["project_id"] = ObjectId(meeting_dict["project_id"])
        
        if "host_id" in meeting_dict and meeting_dict["host_id"]:
            meeting_dict["host_id"] = ObjectId(meeting_dict["host_id"])
        
        if "participant_ids" in meeting_dict and meeting_dict["participant_ids"]:
            meeting_dict["participant_ids"] = [ObjectId(pid) for pid in meeting_dict["participant_ids"]]
        
        # Agregar timestamps
        now = datetime.utcnow()
        meeting_dict["created_at"] = now
        meeting_dict["updated_at"] = now
        
        result = await db[self.collection_name].insert_one(meeting_dict)
        created_meeting = await db[self.collection_name].find_one({"_id": result.inserted_id})
        return created_meeting
    
    async def update(
        self, 
        db: AsyncIOMotorDatabase, 
        meeting_id: str, 
        meeting_in: MeetingUpdate
    ) -> Optional[dict]:
        from datetime import datetime
        
        if not ObjectId.is_valid(meeting_id):
            return None
        
        update_data = meeting_in.model_dump(exclude_unset=True)
        if not update_data:
            return await self.get(db, meeting_id)
        
        if "project_id" in update_data and update_data["project_id"]:
            update_data["project_id"] = ObjectId(update_data["project_id"])
        
        if "host_id" in update_data and update_data["host_id"]:
            update_data["host_id"] = ObjectId(update_data["host_id"])
        
        if "participant_ids" in update_data and update_data["participant_ids"]:
            update_data["participant_ids"] = [ObjectId(pid) for pid in update_data["participant_ids"]]
        
        # Actualizar timestamp
        update_data["updated_at"] = datetime.utcnow()
        
        result = await db[self.collection_name].update_one(
            {"_id": ObjectId(meeting_id)},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            return None
        
        return await self.get(db, meeting_id)
    
    async def delete(self, db: AsyncIOMotorDatabase, meeting_id: str) -> bool:
        if not ObjectId.is_valid(meeting_id):
            return False
        
        result = await db[self.collection_name].delete_one({"_id": ObjectId(meeting_id)})
        return result.deleted_count > 0
    
    async def get_by_jitsi_room(self, db: AsyncIOMotorDatabase, jitsi_room_name: str) -> Optional[dict]:
        meeting_data = await db[self.collection_name].find_one({"jitsi_room_name": jitsi_room_name})
        return meeting_data
    
    async def update_status(self, db: AsyncIOMotorDatabase, meeting_id: str, status: str) -> Optional[dict]:
        if not ObjectId.is_valid(meeting_id):
            return None
        
        await db[self.collection_name].update_one(
            {"_id": ObjectId(meeting_id)},
            {"$set": {"status": status, "updated_at": datetime.utcnow()}}
        )
        
        return await self.get(db, meeting_id)


meeting_crud = MeetingCRUD()
