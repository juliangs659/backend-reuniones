from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional

from app.core.config import settings

# Cliente MongoDB global
mongodb_client: Optional[AsyncIOMotorClient] = None


async def connect_to_mongo():
    """Conectar a MongoDB"""
    global mongodb_client
    mongodb_client = AsyncIOMotorClient(settings.MONGODB_URL)
    print(f"✅ Conectado a MongoDB: {settings.MONGODB_DB}")


async def close_mongo_connection():
    """Cerrar conexión a MongoDB"""
    global mongodb_client
    if mongodb_client:
        mongodb_client.close()
        print("❌ Desconectado de MongoDB")


async def get_database() -> AsyncIOMotorDatabase:
    """Obtener instancia de la base de datos"""
    if mongodb_client is None:
        await connect_to_mongo()
    return mongodb_client[settings.MONGODB_DB]


def get_collection(collection_name: str):
    """Obtener colección de MongoDB de forma síncrona (para uso en contextos no async)"""
    if mongodb_client is None:
        raise Exception("MongoDB no está conectado")
    db = mongodb_client[settings.MONGODB_DB]
    return db[collection_name]
