# V1tr0 Backend API - Sistema de Gestión de Proyectos con IA

Backend API para V1tr0 Dashboard construido con FastAPI, MongoDB y OpenAI para procesamiento inteligente de transcripciones.

## 🚀 Características

- ✅ **FastAPI** - Framework moderno y rápido con async/await
- ✅ **MongoDB** - Base de datos NoSQL con Motor (async driver)
- ✅ **OpenAI Integration** - Procesamiento de transcripciones con IA
- ✅ **Sin autenticación** - API pública (por ahora)
- ✅ **Modelos Pydantic** - Validación de datos robusta
- ✅ **OpenAPI/Swagger** - Documentación automática
- ✅ **Docker Compose** - Despliegue simplificado
- ✅ **Jitsi Meet** - Integración de videollamadas
- ✅ **Redis Cache** - Para mejor rendimiento

## 📋 Requisitos previos

- Python 3.10 o superior
- MongoDB 5.0 o superior
- pip (gestor de paquetes de Python)

## 🔧 Instalación

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd backend_v1tr0
```

### 2. Crear entorno virtual

```bash
python -m venv venv

# En Linux/Mac
source venv/bin/activate

# En Windows
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
cp .env.example .env
```

Edita el archivo `.env` y configura las variables necesarias:

```env
# MongoDB
MONGODB_URL=mongodb://localhost:27017/v1tr0_db
MONGODB_DB=v1tr0_db

# OpenAI (opcional, para funciones de IA)
OPENAI_API_KEY=tu-api-key-aqui
```

### 5. Instalar y configurar MongoDB

#### En Ubuntu/Debian:

```bash
# Importar clave pública de MongoDB
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -

# Crear archivo de lista para MongoDB
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu $(lsb_release -cs)/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# Actualizar repositorios
sudo apt-get update

# Instalar MongoDB
sudo apt-get install -y mongodb-org

# Iniciar MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod

# Verificar estado
sudo systemctl status mongod
```

#### Con Docker:

```bash
# Ejecutar MongoDB en Docker
docker run -d \
  --name mongodb \
  -p 27017:27017 \
  -e MONGO_INITDB_DATABASE=v1tr0_db \
  -v mongodb_data:/data/db \
  mongo:7.0
```

#### Verificar conexión:

```bash
# Conectar a MongoDB
mongosh

# O con Docker
docker exec -it mongodb mongosh

# En el shell de MongoDB:
show dbs
use v1tr0_db
```

## 🚀 Ejecución

### Modo desarrollo (con recarga automática)

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

O simplemente:

```bash
python main.py
```

### Modo producción

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📚 Documentación de la API

Una vez que el servidor esté ejecutándose, puedes acceder a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/api/v1/openapi.json

## 🏗️ Estructura del proyecto

```
backend_v1tr0/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── api.py              # Router principal
│   │       └── endpoints/          # Endpoints REST
│   │           ├── meetings.py              # ✅ Reuniones Jitsi
│   │           ├── transcriptions.py        # ✅ Transcripciones + IA
│   │           ├── project_phases.py        # ✅ Fases de proyectos
│   │           ├── requirements.py          # ✅ Requerimientos
│   │           └── phase_comments.py        # ✅ Comentarios por fase
│   ├── core/
│   │   ├── config.py               # Configuración + OpenAI
│   │   ├── database.py             # Conexión a MongoDB
│   │   └── deps.py                 # Dependencias
│   ├── crud/
│   │   ├── transcription.py        # ✅ CRUD + process_with_ai()
│   │   ├── project_phase.py        # ✅ CRUD + reordenar
│   │   ├── requirement.py          # ✅ CRUD + mover a fase
│   │   └── phase_comment.py        # ✅ CRUD
│   ├── models/
│   │   ├── base.py                 # Modelo base MongoDB
│   │   ├── client.py               # Clientes
│   │   ├── project.py              # Proyectos + fases
│   │   ├── meeting.py              # Reuniones Jitsi
│   │   ├── transcription.py        # ✅ Transcripciones Teams
│   │   ├── project_phase.py        # ✅ Fases del proyecto
│   │   ├── requirement.py          # ✅ Requerimientos extraídos
│   │   └── phase_comment.py        # ✅ Comentarios
│   ├── schemas/
│   │   ├── transcription.py        # ✅ Schemas + ProcessRequest
│   │   ├── project_phase.py        # ✅ Schemas + Reorder
│   │   ├── requirement.py          # ✅ Schemas
│   │   ├── phase_comment.py        # ✅ Schemas
│   │   ├── meeting.py              # Schemas de reuniones
│   │   └── common.py               # Schemas comunes
│   └── services/
│       └── openai_service.py       # ✅ Servicio OpenAI
├── main.py                         # Punto de entrada
├── requirements.txt                # Dependencias
├── .env.example                    # Variables de entorno
├── docker-compose.yml              # Docker: API + MongoDB + Redis
├── API_TESTING_GUIDE.md           # ✅ Guía completa de testing
└── README.md                       # Este archivo
```

## 🔌 Endpoints Implementados

### 📋 **29 Endpoints REST activos:**

#### Transcriptions (6 endpoints)
- `POST /api/v1/transcriptions/` - Subir transcripción de Teams
- `GET /api/v1/transcriptions/` - Listar con filtros
- `GET /api/v1/transcriptions/{id}` - Obtener por ID
- `PUT /api/v1/transcriptions/{id}` - Actualizar
- `DELETE /api/v1/transcriptions/{id}` - Eliminar
- `POST /api/v1/transcriptions/{id}/process` - ⚡ Procesar con IA

#### Project Phases (9 endpoints)
- `POST /api/v1/project-phases/` - Crear fase
- `GET /api/v1/project-phases/` - Listar todas
- `GET /api/v1/project-phases/project/{project_id}` - Por proyecto
- `GET /api/v1/project-phases/{id}` - Obtener por ID
- `PUT /api/v1/project-phases/{id}` - Actualizar
- `DELETE /api/v1/project-phases/{id}` - Eliminar
- `PATCH /api/v1/project-phases/{id}/status` - Actualizar estado
- `PATCH /api/v1/project-phases/{id}/completion` - Actualizar progreso
- `POST /api/v1/project-phases/reorder` - Reordenar fases

#### Requirements (8 endpoints)
- `POST /api/v1/requirements/` - Crear requerimiento
- `GET /api/v1/requirements/` - Listar con filtros
- `GET /api/v1/requirements/phase/{phase_id}` - Por fase
- `GET /api/v1/requirements/{id}` - Obtener por ID
- `PUT /api/v1/requirements/{id}` - Actualizar
- `DELETE /api/v1/requirements/{id}` - Eliminar
- `PATCH /api/v1/requirements/{id}/status` - Actualizar estado
- `PATCH /api/v1/requirements/{id}/move` - Mover a otra fase

#### Phase Comments (6 endpoints)
- `POST /api/v1/phase-comments/` - Comentar fase
- `GET /api/v1/phase-comments/` - Listar
- `GET /api/v1/phase-comments/phase/{phase_id}` - Por fase
- `GET /api/v1/phase-comments/{id}` - Obtener por ID
- `PUT /api/v1/phase-comments/{id}` - Actualizar
- `DELETE /api/v1/phase-comments/{id}` - Eliminar

### Health Check

```bash
# Verificar estado de la API
curl http://localhost:8000/health
# Respuesta: {"status":"healthy","database":"MongoDB"}

# Documentación interactiva
# http://localhost:8000/docs
```

📚 **Ver guía completa:** [API_TESTING_GUIDE.md](API_TESTING_GUIDE.md)

## 🗄️ Colecciones de MongoDB

El proyecto utiliza las siguientes colecciones:

- `clients` - Clientes del sistema
- `projects` - Proyectos con fases
- `meetings` - Reuniones Jitsi
- `transcriptions` - ✅ Transcripciones de Teams + análisis IA
- `project_phases` - ✅ Fases del proyecto
- `requirements` - ✅ Requerimientos extraídos por IA
- `phase_comments` - ✅ Comentarios por fase

## 🔍 Operaciones con MongoDB

### Conectar a MongoDB:

```bash
mongosh mongodb://localhost:27017/v1tr0_db
```

### Comandos útiles:

```javascript
// Ver todas las colecciones
show collections

// Ver documentos de una colección
db.users.find().pretty()

// Contar documentos
db.projects.countDocuments()

// Crear índices para mejor rendimiento
db.transcriptions.createIndex({ user_email: 1 })
db.transcriptions.createIndex({ project_id: 1 })
db.project_phases.createIndex({ project_id: 1, order: 1 })
db.requirements.createIndex({ phase_id: 1 })
db.phase_comments.createIndex({ phase_id: 1 })

// Eliminar todos los documentos de una colección
db.transcriptions.deleteMany({})
```

## 🐳 Docker

### Ejecutar con Docker Compose:

```bash
# Iniciar todos los servicios
sudo docker compose up -d

# Ver logs
sudo docker compose logs -f

# Detener servicios
sudo docker compose down
```

## 🧪 Testing

```bash
# Ejecutar tests
pytest

# Con cobertura
pytest --cov=app tests/
```

## 📦 Dependencias principales

- **FastAPI 0.104.1** - Framework web async
- **Motor 3.3.2** - Driver asíncrono de MongoDB
- **Pydantic 2.5.0** - Validación de datos con type hints
- **Uvicorn** - Servidor ASGI de alto rendimiento
- **OpenAI** - Cliente para API de OpenAI (Whisper, GPT-4)
- **Redis** - Cache y pub/sub
- **PyMongo 4.6.1** - Cliente de MongoDB

## 🤖 Integración con OpenAI

El sistema procesa transcripciones de Microsoft Teams usando OpenAI para:

✅ **Extracción automática de:**
- Resumen ejecutivo de la reunión
- Fases del proyecto identificadas
- Requerimientos (funcionales, no funcionales, técnicos)
- Decisiones técnicas tomadas
- Action items pendientes

⚠️ **Configuración requerida:**
```bash
# En tu archivo .env
OPENAI_API_KEY=sk-tu-api-key-real
OPENAI_MODEL=gpt-4-turbo-preview
```

Sin la API key configurada, el sistema funcionará normalmente pero el endpoint `/process` devolverá error.

## 🔐 Seguridad

⚠️ **Nota importante**: Este proyecto NO incluye autenticación de usuarios. La API es pública.

**Para producción, considera implementar:**
- JWT tokens
- OAuth2
- API Keys
- Rate limiting
- Validación de IPs

## 🛠️ Desarrollo

### Formatear código:

```bash
black app/
isort app/
```

### Linting:

```bash
flake8 app/
mypy app/
```

## 📝 Variables de entorno

| Variable | Descripción | Por defecto |
|----------|-------------|-------------|
| `PROJECT_NAME` | Nombre del proyecto | `V1tr0 Backend API` |
| `VERSION` | Versión de la API | `1.0.0` |
| `API_V1_STR` | Prefijo de la API | `/api/v1` |
| `MONGODB_URL` | URL de conexión a MongoDB | `mongodb://localhost:27017/v1tr0_db` |
| `MONGODB_DB` | Nombre de la base de datos | `v1tr0_db` |
| `OPENAI_API_KEY` | **API Key de OpenAI** (requerida para IA) | `tu-api-key-aqui` |
| `OPENAI_MODEL` | Modelo de OpenAI | `gpt-4-turbo-preview` |
| `REDIS_URL` | URL de Redis | `redis://localhost:6379` |
| `BACKEND_CORS_ORIGINS` | Orígenes permitidos para CORS | `["http://localhost:3000"]` |
| `JITSI_DOMAIN` | Dominio de Jitsi Meet | `meet.jit.si` |
| `LOG_LEVEL` | Nivel de logging | `INFO` |
| `ENVIRONMENT` | Entorno (dev/prod) | `development` |

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT.

## 📞 Soporte

Si tienes problemas o preguntas, por favor abre un issue en el repositorio.

---

**¡Desarrollado con ❤️ usando FastAPI y MongoDB!**
