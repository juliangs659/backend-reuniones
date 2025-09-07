from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import verify_supabase_token, decode_token
from app.models.user import User
from app.crud.crud_user import user_crud

security = HTTPBearer()


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """Obtener usuario actual desde el token"""
    token = credentials.credentials
    
    try:
        # Verificar token con Supabase
        supabase_user = await verify_supabase_token(token)
        
        # Buscar o crear usuario en nuestra base de datos
        user = await user_crud.get_by_supabase_id(db, supabase_id=supabase_user["id"])
        
        if not user:
            # Crear usuario si no existe
            user_data = {
                "supabase_id": supabase_user["id"],
                "email": supabase_user["email"],
                "full_name": supabase_user.get("user_metadata", {}).get("full_name", ""),
                "is_active": True
            }
            user = await user_crud.create(db, obj_in=user_data)
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuario inactivo"
            )
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudo validar las credenciales",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Obtener usuario activo actual"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario inactivo"
        )
    return current_user


async def get_current_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Obtener usuario administrador actual"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos suficientes"
        )
    return current_user


async def get_optional_current_user(
    db: AsyncSession = Depends(get_db),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[User]:
    """Obtener usuario actual opcional (para endpoints públicos)"""
    if not credentials:
        return None
    
    try:
        return await get_current_user(db, credentials)
    except HTTPException:
        return None