from typing import AsyncGenerator
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.database import get_database


async def get_db() -> AsyncGenerator[AsyncIOMotorDatabase, None]:
    """Dependencia para obtener la base de datos de MongoDB"""
    db = await get_database()
    try:
        yield db
    finally:
        pass