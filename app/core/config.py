from typing import List, Optional, Union
from pydantic_settings import BaseSettings
from pydantic import field_validator
import os
from functools import lru_cache


class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # Información del proyecto
    PROJECT_NAME: str = "V1tr0 Backend API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # MongoDB
    MONGODB_URL: Optional[str] = None
    MONGODB_SERVER: str = "localhost"
    MONGODB_PORT: int = 27017
    MONGODB_DB: str = "v1tr0_db"
    MONGODB_USER: Optional[str] = None
    MONGODB_PASSWORD: Optional[str] = None
    
    @field_validator("MONGODB_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], info) -> str:
        if isinstance(v, str) and v:
            return v
        
        values = info.data
        user = values.get('MONGODB_USER')
        password = values.get('MONGODB_PASSWORD')
        server = values.get('MONGODB_SERVER', 'localhost')
        port = values.get('MONGODB_PORT', 27017)
        
        if user and password:
            return f"mongodb://{user}:{password}@{server}:{port}/{values.get('MONGODB_DB', 'v1tr0_db')}"
        return f"mongodb://{server}:{port}/{values.get('MONGODB_DB', 'v1tr0_db')}"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "https://localhost:3000",
        "https://localhost:3001",
    ]
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Hosts permitidos
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1", "0.0.0.0"]
    
    # OpenAI (para procesamiento de transcripciones y IA)
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o-mini"  # Modelo económico y eficiente
    
    # Jitsi Meet
    JITSI_DOMAIN: str = "meet.jit.si"
    JITSI_APP_ID: Optional[str] = None
    JITSI_PRIVATE_KEY: Optional[str] = None
    
    # Redis (para cache y sesiones)
    REDIS_URL: str = "redis://localhost:6379"
    
    # Configuración de logging
    LOG_LEVEL: str = "INFO"
    
    # Entorno
    ENVIRONMENT: str = "development"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Obtener configuración singleton"""
    return Settings()


settings = get_settings()