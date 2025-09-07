from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool
from typing import AsyncGenerator

from app.core.config import settings

# Crear el motor de base de datos asíncrono
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,  # Cambiar a False en producción
    future=True,
    poolclass=NullPool,  # Para desarrollo, usar pool apropiado en producción
)

# Crear el sessionmaker asíncrono
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Base para los modelos
Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependencia para obtener sesión de base de datos"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """Inicializar la base de datos"""
    async with engine.begin() as conn:
        # Crear todas las tablas
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """Cerrar conexiones de base de datos"""
    await engine.dispose()