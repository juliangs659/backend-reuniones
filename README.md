# V1tr0 Backend API

## 📋 Descripción

Backend API desarrollado en FastAPI para el dashboard de gestión de proyectos V1tr0. Proporciona una API REST completa para la gestión de proyectos, clientes, reuniones, transcripciones de audio y chat con IA.

## 🏗️ Arquitectura

### Tecnologías Principales

- **FastAPI**: Framework web moderno y rápido para Python
- **SQLAlchemy**: ORM asíncrono para base de datos
- **PostgreSQL**: Base de datos principal
- **Supabase**: Autenticación y gestión de usuarios
- **OpenAI**: Procesamiento de IA para transcripciones y chat
- **Jitsi Meet**: Integración para videollamadas
- **Redis**: Cache y gestión de sesiones

### Estructura del Proyecto

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/          # Endpoints de la API
│   │       │   ├── auth.py
│   │       │   ├── users.py
│   │       │   ├── projects.py
│   │       │   ├── clients.py
│   │       │   ├── meetings.py
│   │       │   ├── transcriptions.py
│   │       │   └── ai_chat.py
│   │       └── api.py              # Router principal
│   ├── core/
│   │   ├── config.py               # Configuración
│   │   ├── database.py             # Configuración de BD
│   │   ├── security.py             # Autenticación y seguridad
│   │   └── deps.py                 # Dependencias
│   ├── crud/                       # Operaciones CRUD
│   │   ├── crud_user.py
│   │   ├── crud_client.py
│   │   ├── crud_project.py
│   │   ├── crud_meeting.py
│   │   ├── crud_transcription.py
│   │   └── crud_chat_message.py
│   ├── models/                     # Modelos SQLAlchemy
│   │   ├── base.py
│   │   ├── user.py
│   │   ├── client.py
│   │   ├── project.py
│   │   ├── meeting.py
│   │   ├── transcription.py
│   │   └── chat_message.py
│   ├── schemas/                    # Esquemas Pydantic
│   │   ├── common.py
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── client.py
│   │   ├── project.py
│   │   ├── meeting.py
│   │   ├── transcription.py
│   │   └── chat_message.py
│   ├── services/                   # Lógica de negocio
│   │   ├── auth_service.py
│   │   ├── ai_service.py
│   │   ├── transcription_service.py
│   │   ├── meeting_service.py
│   │   └── notification_service.py
│   └── utils/                      # Utilidades
│       ├── audio_processing.py
│       ├── file_handling.py
│       └── validators.py
├── alembic/                        # Migraciones de BD
├── uploads/                        # Archivos subidos
├── tests/                          # Tests
├── main.py                         # Punto de entrada
├── requirements.txt                # Dependencias
├── .env.example                    # Variables de entorno
└── README.md
```

## 🚀 Funcionalidades Principales

### 1. Autenticación y Usuarios
- Integración con Supabase para autenticación
- Gestión de perfiles de usuario
- Control de acceso basado en roles
- JWT tokens para autorización

### 2. Gestión de Proyectos
- CRUD completo de proyectos
- Seguimiento de progreso y estado
- Gestión de presupuestos y horas
- Filtros y búsqueda avanzada
- Estadísticas y métricas

### 3. Gestión de Clientes
- CRUD completo de clientes
- Información de contacto y facturación
- Historial de proyectos por cliente
- Segmentación y priorización

### 4. Sistema de Reuniones
- Integración con Jitsi Meet
- Programación y gestión de reuniones
- Grabación automática
- Gestión de participantes
- URLs de acceso seguras

### 5. Transcripciones de Audio
- Procesamiento automático con OpenAI Whisper
- Generación de resúmenes con IA
- Extracción de puntos clave
- Identificación de compromisos y próximos pasos
- Detección de participantes

### 6. Chat con IA Contextual
- Chat inteligente por proyecto
- Contexto basado en transcripciones y datos del proyecto
- Búsqueda semántica en el historial
- Generación de insights y recomendaciones
- Historial de conversaciones

## 🔧 Configuración

### Variables de Entorno

Copia `.env.example` a `.env` y configura las siguientes variables:

```bash
# Base de datos
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/v1tr0_db

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# OpenAI
OPENAI_API_KEY=sk-your-openai-api-key

# JWT
SECRET_KEY=your-super-secret-key

# Redis
REDIS_URL=redis://localhost:6379
```

### Instalación

1. **Crear entorno virtual:**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

3. **Configurar base de datos:**
```bash
# Crear base de datos PostgreSQL
createdb v1tr0_db

# Ejecutar migraciones
alembic upgrade head
```

4. **Ejecutar servidor de desarrollo:**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📚 API Endpoints

### Autenticación
- `POST /api/v1/auth/login` - Iniciar sesión
- `POST /api/v1/auth/register` - Registrar usuario
- `GET /api/v1/auth/me` - Obtener usuario actual
- `POST /api/v1/auth/refresh` - Renovar token

### Usuarios
- `GET /api/v1/users/` - Listar usuarios
- `GET /api/v1/users/{id}` - Obtener usuario
- `PUT /api/v1/users/{id}` - Actualizar usuario
- `GET /api/v1/users/{id}/stats` - Estadísticas de usuario

### Proyectos
- `GET /api/v1/projects/` - Listar proyectos
- `POST /api/v1/projects/` - Crear proyecto
- `GET /api/v1/projects/{id}` - Obtener proyecto
- `PUT /api/v1/projects/{id}` - Actualizar proyecto
- `DELETE /api/v1/projects/{id}` - Eliminar proyecto
- `GET /api/v1/projects/{id}/stats` - Estadísticas de proyecto

### Clientes
- `GET /api/v1/clients/` - Listar clientes
- `POST /api/v1/clients/` - Crear cliente
- `GET /api/v1/clients/{id}` - Obtener cliente
- `PUT /api/v1/clients/{id}` - Actualizar cliente
- `DELETE /api/v1/clients/{id}` - Eliminar cliente
- `GET /api/v1/clients/{id}/projects` - Proyectos del cliente

### Reuniones
- `GET /api/v1/meetings/` - Listar reuniones
- `POST /api/v1/meetings/` - Crear reunión
- `GET /api/v1/meetings/{id}` - Obtener reunión
- `PUT /api/v1/meetings/{id}` - Actualizar reunión
- `POST /api/v1/meetings/{id}/join` - Unirse a reunión
- `POST /api/v1/meetings/{id}/leave` - Salir de reunión

### Transcripciones
- `GET /api/v1/transcriptions/` - Listar transcripciones
- `POST /api/v1/transcriptions/upload/{meeting_id}` - Subir audio
- `GET /api/v1/transcriptions/{id}` - Obtener transcripción
- `POST /api/v1/transcriptions/{id}/regenerate-summary` - Regenerar resumen

### Chat con IA
- `POST /api/v1/ai/chat/{project_id}` - Enviar mensaje
- `GET /api/v1/ai/chat/{project_id}` - Historial de chat
- `GET /api/v1/ai/ask/{project_id}` - Hacer pregunta específica
- `GET /api/v1/ai/insights/{project_id}` - Obtener insights
- `GET /api/v1/ai/search/{project_id}` - Búsqueda semántica

## 🔒 Seguridad

- **Autenticación**: Integración con Supabase
- **Autorización**: JWT tokens con roles
- **CORS**: Configurado para el frontend
- **Rate Limiting**: Protección contra abuso
- **Validación**: Esquemas Pydantic estrictos
- **Sanitización**: Limpieza de datos de entrada

## 🧪 Testing

```bash
# Ejecutar tests
pytest

# Con cobertura
pytest --cov=app

# Tests específicos
pytest tests/test_projects.py
```

## 📊 Monitoreo

- **Logs**: Configuración con Loguru
- **Métricas**: Endpoints de salud y métricas
- **Documentación**: Swagger UI automática en `/docs`
- **Redoc**: Documentación alternativa en `/redoc`

## 🚀 Despliegue

### Docker

```dockerfile
# Dockerfile incluido para containerización
docker build -t v1tr0-backend .
docker run -p 8000:8000 v1tr0-backend
```

### Variables de Producción

```bash
# Configuración para producción
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
```

## 🔄 Integración con Frontend

El backend está diseñado para integrarse perfectamente con el frontend Next.js existente:

- **API Compatible**: Endpoints que coinciden con las llamadas del frontend
- **Tipos TypeScript**: Esquemas Pydantic generan tipos compatibles
- **CORS Configurado**: Permite requests desde el frontend
- **WebSockets**: Para actualizaciones en tiempo real (futuro)

## 📈 Roadmap

- [ ] WebSockets para actualizaciones en tiempo real
- [ ] Sistema de notificaciones
- [ ] Integración con calendarios externos
- [ ] API de webhooks
- [ ] Dashboard de analytics
- [ ] Exportación de reportes
- [ ] Integración con herramientas de gestión de proyectos

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 📞 Soporte

Para soporte técnico o preguntas:
- Email: soporte@v1tr0.com
- Documentación: [docs.v1tr0.com](https://docs.v1tr0.com)
- Issues: [GitHub Issues](https://github.com/v1tr0/backend/issues)